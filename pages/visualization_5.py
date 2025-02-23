import streamlit as st
import pandas as pd
import json
from collections import defaultdict
from itertools import combinations

def safe_str(val):
    """NaN 등을 빈 문자열로 안전 처리"""
    if pd.isna(val):
        return ""
    return str(val).strip()

def map_category(cat):
    """
    CSV의 category값을 사람이 읽기 좋은 형태로 변환
    """
    if cat == "oscar":
        return "Oscar"
    elif cat == "palme_dor":
        return "Palme d'Or"
    elif cat == "golden_globe":
        return "Golden Globes"
    else:
        return cat

def main():
    st.set_page_config(layout="wide")
    st.title("🏆 수상 데이터 분석")

    df = pd.read_csv("data/2-5.csv")

    edge_dict = {}
    person_info = {}
    person_movies_set = defaultdict(lambda: defaultdict(set))

    # 1) CSV 순회
    for idx, row in df.iterrows():
        director = safe_str(row.get("director", ""))
        cast1 = safe_str(row.get("cast1", ""))
        cast2 = safe_str(row.get("cast2", ""))
        cast3 = safe_str(row.get("cast3", ""))

        dir_img = safe_str(row.get("image_director", ""))
        c1_img = safe_str(row.get("image_cast1", ""))
        c2_img = safe_str(row.get("image_cast2", ""))
        c3_img = safe_str(row.get("image_cast3", ""))

        movie_title = safe_str(row.get("title", ""))
        movie_img = safe_str(row.get("image_title", ""))

        cat = safe_str(row.get("category", ""))

        people = []
        if director:
            people.append(director)
            if director not in person_info:
                person_info[director] = {"role": "director", "image": dir_img}
            else:
                if person_info[director]["role"] == "actor":
                    person_info[director]["role"] = "director"
                if not person_info[director]["image"] and dir_img:
                    person_info[director]["image"] = dir_img

        for cast_name, cast_img in [(cast1, c1_img), (cast2, c2_img), (cast3, c3_img)]:
            if cast_name:
                if cast_name not in person_info:
                    person_info[cast_name] = {"role": "actor", "image": cast_img}
                else:
                    if not person_info[cast_name]["image"] and cast_img:
                        person_info[cast_name]["image"] = cast_img
                people.append(cast_name)

        # 영화/카테고리 정보
        for p in people:
            person_movies_set[p][(movie_title, movie_img)].add(cat)

        # 같은 영화에 나온 사람들끼리 연결
        for p1, p2 in combinations(people, 2):
            p1, p2 = sorted([p1, p2])
            edge_dict[(p1, p2)] = edge_dict.get((p1, p2), 0) + 1

    # 2) 차수 계산
    degree_dict = {}
    for (p1, p2), weight in edge_dict.items():
        degree_dict[p1] = degree_dict.get(p1, 0) + weight
        degree_dict[p2] = degree_dict.get(p2, 0) + weight

    # 3) 검색창
    search_name = st.text_input("감독 또는 배우 이름을 검색하세요")

    # 4) 노드
    nodes_data = []
    for person, info in person_info.items():
        deg = degree_dict.get(person, 0)
        # 노드 크기 무제한 (상한 없음)
        size_val = 20 + deg * 3

        shape_type = "circularImage" if info["image"] else "dot"

        node_item = {
            "id": person,
            "label": person,
            "shape": shape_type,
            "role": info["role"],
            "size": size_val,
            "borderWidth": 4,
            "hidden": False
        }
        if info["image"]:
            node_item["image"] = info["image"]

        if info["role"] == "director":
            node_item["color"] = {
                "border": "#FFD700",
                "background": "#ffffff"
            }
        else:
            node_item["color"] = {
                "border": "#66CCFF",
                "background": "#ffffff"
            }

        nodes_data.append(node_item)

    # 5) 에지
    edges_data = []
    edge_id = 0
    for (p1, p2), weight in edge_dict.items():
        d1 = degree_dict.get(p1, 1)
        d2 = degree_dict.get(p2, 1)
        # ★ 기존 (1 + 0.3*(d1+d2))에서 2배로
        w = 2.5 * (1 + 0.3 * (d1 + d2))  
        edges_data.append({
            "id": f"edge_{edge_id}",
            "from": p1,
            "to": p2,
            "width": w,
            "color": "rgba(128,128,128,0.3)",
            "hidden": False
        })
        edge_id += 1

    # 6) 검색 기능
    if search_name:
        if search_name in person_info:
            neighbors = set()
            neighbors.add(search_name)
            for (a, b), wt in edge_dict.items():
                if a == search_name:
                    neighbors.add(b)
                if b == search_name:
                    neighbors.add(a)

            for nd in nodes_data:
                if nd["id"] in neighbors:
                    nd["hidden"] = False
                else:
                    nd["hidden"] = True

            for ed in edges_data:
                p1 = ed["from"]
                p2 = ed["to"]
                if (p1 in neighbors) and (p2 in neighbors):
                    ed["hidden"] = False
                else:
                    ed["hidden"] = True
        else:
            st.warning(f"'{search_name}' not found. Showing all.")
            pass
    else:
        pass

    # 7) 팝업 데이터
    person_movies_map = {}
    for person, mov_dict in person_movies_set.items():
        mov_list = []
        for (mtitle, mimg), cat_set in mov_dict.items():
            cat_list = sorted([map_category(c) for c in cat_set if c])
            cat_str = ", ".join(cat_list)
            mov_list.append({
                "title": mtitle,
                "image": mimg,
                "categories": cat_str
            })
        person_movies_map[person] = mov_list

    # 8) HTML
    html_code = create_visjs_html(nodes_data, edges_data, person_movies_map)
    st.components.v1.html(html_code, height=1200, scrolling=True)

def create_visjs_html(nodes, edges, person_movies_map):
    import json
    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)
    movies_json = json.dumps(person_movies_map, ensure_ascii=False)

    html_code = """
<html>
<head>
  <meta charset="utf-8"/>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto&display=swap">
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    /* 전체 페이지 배경을 연한 베이지(#f5f5dc)로 */
    html, body {
      margin: 0; 
      padding: 0;
      height: 100%;
      font-family: 'Roboto', sans-serif;
      background-color: #f5f5dc; /* 연한 베이지색 */
    }
    #mynetwork {
      width: 100%;
      height: 100%;
      /* 이쁜 테두리와 배경 */
      background: #f5f5dc; /* 베이지색 배경 */
      border: 2px solid #e0c9a6; /* 좀 더 어울리는 테두리색 */
      border-radius: 10px; /* 둥근 모서리 */
      box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* 은은한 그림자 */
      position: relative;
    }
    #popup {
      position: absolute;
      display: none;
      background: #ffffff;
      color: #333;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 12px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
      z-index: 9999;
      max-width: 300px;
      font-family: 'Roboto', sans-serif;
      font-size: 14px;
      line-height: 1.4;
    }
    #popup::before {
      content: "";
      position: absolute;
      bottom: -15px;
      left: 20px;
      border-left: 8px solid transparent;
      border-right: 8px solid transparent;
      border-top: 8px solid #ffffff;
    }
    #popup img {
      max-width: 60px;
      margin-right: 5px;
      vertical-align: middle;
      border-radius: 4px;
    }
    .vis-network div.vis-label {
      font-family: 'Roboto', sans-serif;
      font-size: 14px;
      color: #000000;
    }
  </style>
</head>
<body>
  <div id="mynetwork"></div>
  <div id="popup"></div>
  <script>
    var nodesData = REPLACE_NODES_DATA;
    var edgesData = REPLACE_EDGES_DATA;
    var personMoviesMap = REPLACE_MOVIES_DATA;

    var nodes = new vis.DataSet(nodesData);
    var edges = new vis.DataSet(edgesData);

    var container = document.getElementById('mynetwork');
    var data = {
      nodes: nodes,
      edges: edges
    };

    var options = {
      physics: {
        enabled: true,
        solver: "barnesHut",
        barnesHut: {
          avoidOverlap: 0.8,
          centralGravity: 0.1,
          springLength: 350,
          springConstant: 0.04,
          damping: 0.09
        }
      },
      edges: {
        smooth: false
      },
      interaction: {
        dragNodes: true,
        hover: true
      }
    };

    var network = new vis.Network(container, data, options);

    var popup = document.getElementById("popup");

    function hidePopup() {
      popup.style.display = "none";
    }

    function showPopup(personId, x, y) {
      var movies = personMoviesMap[personId] || [];
      if (movies.length === 0) {
        popup.innerHTML = "<b>" + personId + "</b><br/>No movie info.";
      } else {
        var html = "<b>" + personId + "</b><br/>";
        for (var i = 0; i < movies.length; i++) {
          var t = movies[i].title || "Untitled";
          var img = movies[i].image || "";
          var catStr = movies[i].categories || "";

          html += "<div style='margin-bottom:5px;'>";
          if (img) {
            html += "<img src='" + img + "' />";
          }
          if (catStr) {
            html += t + " (" + catStr + ")";
          } else {
            html += t;
          }
          html += "</div>";
        }
        popup.innerHTML = html;
      }
      popup.style.left = (x + 10) + "px";
      popup.style.top = (y + 10) + "px";
      popup.style.display = "block";
    }

    // 노드 클릭 -> 그 노드와 연결된 노드만 보이고, 나머지는 hidden
    function focusNodeAndNeighbors(nodeId) {
      var connectedNodes = network.getConnectedNodes(nodeId);
      var connectedEdges = network.getConnectedEdges(nodeId);
      connectedNodes.push(nodeId);

      var allNodes = nodes.get();
      for (var i = 0; i < allNodes.length; i++) {
        var n = allNodes[i];
        if (connectedNodes.indexOf(n.id) !== -1) {
          n.hidden = false;
        } else {
          n.hidden = true;
        }
      }
      nodes.update(allNodes);

      var allEdges = edges.get();
      for (var j = 0; j < allEdges.length; j++) {
        var e = allEdges[j];
        if (connectedEdges.indexOf(e.id) !== -1) {
          e.hidden = false;
        } else {
          e.hidden = true;
        }
      }
      edges.update(allEdges);
    }

    function showAll() {
      var allNodes = nodes.get();
      for (var i = 0; i < allNodes.length; i++) {
        allNodes[i].hidden = false;
      }
      nodes.update(allNodes);

      var allEdges = edges.get();
      for (var j = 0; j < allEdges.length; j++) {
        allEdges[j].hidden = false;
      }
      edges.update(allEdges);
    }

    // 노드 클릭 시 해당 노드 + 연결된 노드만
    network.on("click", function(params) {
      hidePopup();
      if (params.nodes.length > 0) {
        var clickedId = params.nodes[0];
        focusNodeAndNeighbors(clickedId);
        showPopup(clickedId, params.pointer.DOM.x, params.pointer.DOM.y);
      } else {
        showAll();
      }
    });

    network.on("dragStart", function(params) {
      hidePopup();
    });
  </script>
</body>
</html>
"""
    # 치환
    html_code = html_code.replace("REPLACE_NODES_DATA", nodes_json)
    html_code = html_code.replace("REPLACE_EDGES_DATA", edges_json)
    html_code = html_code.replace("REPLACE_MOVIES_DATA", movies_json)

    return html_code

if __name__ == "__main__":
    main()
