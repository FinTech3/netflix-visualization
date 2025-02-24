import streamlit as st
import pandas as pd
import folium
import requests
import country_converter as coco  # 국가 이름을 코드로 변환
from streamlit_folium import st_folium
import os
import numpy as np
import json
from branca.colormap import linear  # 색상 매핑을 위한 라이브러리

# 📌 Streamlit UI
st.title("Netflix 주간별 Top 1 Visualization")

# 🌍 국가별 위도/경도 데이터 (ISO 코드 기반) - 캐싱
@st.cache_data
def get_country_coords():
    iso_codes = [
        "AR", "AU", "AT", "BS", "BH", "BD", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "HR", "CY", "CZ", "DK",
        "DO", "EC", "EG", "SV", "EE", "FI", "FR", "DE", "GR", "GP", "GT", "HN", "HK", "HU", "IS", "IN", "ID", "IE",
        "IL", "IT", "JM", "JP", "JO", "KE", "KW", "LV", "LB", "LT", "LU", "MY", "MV", "MT", "MQ", "MU", "MX", "MA",
        "NL", "NC", "NZ", "NI", "NG", "NO", "OM", "PK", "PA", "PY", "PE", "PH", "PL", "PT", "QA", "RO", "RE", "SA",
        "RS", "SG", "SK", "SI", "ZA", "KR", "ES", "LK", "SE", "CH", "TW", "TH", "TT", "TR", "UA", "AE", "GB", "US",
        "UY", "VE", "VN","RU"
    ]

    latitudes = [
        -38.4161, -25.2744, 47.5162, 25.0343, 26.0667, 23.685, 50.8503, -16.5000, -14.235, 42.7339, 56.1304, -35.6751,
        4.5709, 9.7489, 45.1000, 35.1264, 49.8175, 56.2639, 18.7357, -1.8312, 26.8206, 13.6929, 58.5953, 61.9241,
        48.8566, 51.1657, 39.0742, 16.2650, 15.7835, 15.2000, 22.3193, 47.1625, 64.9631, 20.5937, -0.7893, 53.4129,
        31.0461, 41.8719, 18.1096, 35.6828, 31.9632, -1.2864, 29.3759, 56.8796, 33.8547, 55.1694, 49.8153, 4.2105,
        3.2028, 35.8997, 14.6415, -20.3484, 23.6345, 31.7917, 52.3676, -20.9043, -40.9006, 12.8654, 9.0820, 60.4720,
        21.5126, 30.3753, 8.9824, -23.4425, -9.1900, 13.4125, 51.9194, 39.3999, 25.3548, 45.9432, -21.1151, 23.8859,
        44.0165, 1.3521, 48.6690, 46.1512, -30.5595, 37.5665, 40.4637, 7.8731, 60.1282, 46.8182, 23.6978, 15.8700,
        10.6918, 38.9637, 48.3794, 25.2760, 55.3781, 37.0902, -32.5228, 6.4238, 14.0583, 61.5240
    ]

    longitudes = [
        -63.6167, 133.7751, 14.5501, -77.3963, 50.5577, 90.3563, 4.3517, -68.1500, -51.9253, 25.4858, -106.3468,
        -71.5429, -74.2973, -83.7534, 15.2000, 33.4299, 15.4720, 9.5018, -70.1627, -78.1834, 30.8025, -89.2182,
        25.0136, 25.7482, 2.3522, 10.4515, 21.8243, -61.5500, -90.2308, -86.2419, 114.1694, 19.5033, -19.0208,
        78.9629, 113.9213, -8.2439, 34.8516, 12.5674, -77.2975, 139.7595, 35.9304, 36.8219, 47.6581, 24.6032,
        35.8623, 23.8813, 114.1512, 101.9758, 73.2207, 14.3754, -61.0242, 57.5522, -102.5528, -7.0926, 4.9041,
        165.6180, 172.6362, -85.2072, 8.6753, 8.4689, 55.9233, 69.3451, -79.5199, -58.4438, -75.0152, 121.7740,
        19.1451, -8.2245, 51.1839, 24.9668, 45.0792, 44.4249, 46.1512, 22.9375, 103.8198, 19.6990, 14.9955, 126.9780,
        -30.5595, 126.9780, -3.7038, 80.7718, 18.6435, 8.2275, 120.9605, 100.9925, 31.1656, 35.2433, 31.1656,
        -95.7129, -3.4360, -95.7129, -55.7658, 105.3188
    ]
    return pd.DataFrame({"country_iso2": iso_codes, "latitude": latitudes, "longitude": longitudes})

# 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return (
        pd.read_csv(os.path.join(base_path, "2-2_movies.csv")),
        pd.read_csv(os.path.join(base_path, "2-2_tv.csv")),
    )

# 🏆 1위 작품만 필터링
movies_df, series_df = load_data()
movies_df["content_type"] = "Movie"  # 영화
series_df["content_type"] = "TV"  # TV
top1_df = pd.concat([movies_df[movies_df["weekly_rank"] == 1], series_df[series_df["weekly_rank"] == 1]], ignore_index=True)

# 국가 데이터 병합
country_coords = get_country_coords()
top1_df = top1_df.merge(country_coords, on="country_iso2", how="left")

# 📅 주간 목록
weeks = sorted(top1_df["week"].unique(), reverse=True)

# 📌 주간 선택
selected_week = st.selectbox("주간을 선택하세요:", weeks)

# 📌 콘텐츠 유형 선택 (영화/TV)
content_options = ["Movie", "TV"]
selected_content = st.radio("콘텐츠 유형을 선택하세요:", content_options, horizontal=True)

# 🏆 주간별 데이터 필터링 (캐싱)
@st.cache_data
def filter_week_data(week, content_type):
    week_df = top1_df[(top1_df["week"] == week) & (top1_df["content_type"] == content_type)].copy()
    
    # ✅ 각 작품이 몇 개의 서로 다른 국가에서 1위를 했는지 계산
    weekly_counts = week_df.groupby("show_title")["country_iso2"].nunique()
    
    # ✅ 글로벌 히트 수정: 2개 이상의 서로 다른 국가에서 1위를 해야 글로벌 히트
    week_df["category"] = week_df["show_title"].map(lambda x: "Global Hit" if weekly_counts[x] >= 2 else "National Hit")
    
    # ✅ 글로벌 히트 작품의 국가 개수를 저장 (각 작품이 몇 개 나라에서 1위를 했는지)
    week_df["global_hit_count"] = week_df["show_title"].map(lambda x: weekly_counts[x] if weekly_counts[x] >= 2 else 1)
    
    return week_df

week_df = filter_week_data(selected_week, selected_content)

# 🌍 국가별 1위를 한 작품의 국가 수 계산
country_hit_counts = week_df.groupby(["country_iso2", "category"])["global_hit_count"].sum().reset_index(name="count")

# ✅ 색상 설정 (국가 히트: 연한 초록 / 글로벌 히트: 연한 핑크)
color_map = {"National Hit": "#90EE90", "Global Hit": "lightpink"}

# 🏆 국가별 1위 작품 개수 데이터 준비
country_hit_counts_map = week_df.groupby("country_iso2")["global_hit_count"].sum().reset_index()

# 🌍 국가명을 Alpha-3 코드로 변환 (Folium Choropleth는 Alpha-3 코드 사용)
country_hit_counts_map["country_alpha3"] = coco.convert(names=country_hit_counts_map["country_iso2"], to="ISO3")

# 📌 Choropleth 색상 맵 설정 (1위를 많이 한 나라일수록 색이 짙어짐)
colormap = linear.YlOrRd_09.scale(
    country_hit_counts_map["global_hit_count"].min(),
    country_hit_counts_map["global_hit_count"].max()
)

# 🌍 세계 지도 GeoJSON 데이터 로드
world_geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
world_geojson = json.loads(requests.get(world_geojson_url).text)

# 🗺️ Folium 지도 생성
m = folium.Map(location=[20, 0], zoom_start=2)

# 🌍 Choropleth 지도 추가 (국가별 1위 개수에 따라 색칠)
folium.Choropleth(
    geo_data=world_geojson,
    name="Choropleth",
    data=country_hit_counts_map,
    columns=["country_alpha3", "global_hit_count"],
    key_on="feature.id",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="국가별 Netflix 1위 작품 개수",
    highlight=True,
    nan_fill_color="#D3D3D3"
).add_to(m)

# 🗺️ 기존 원형 마커도 추가
for _, row in country_hit_counts.iterrows():
    country_info = country_coords[country_coords["country_iso2"] == row["country_iso2"]]
    if not country_info.empty:
        lat, lon = country_info.iloc[0]["latitude"], country_info.iloc[0]["longitude"]

        radius = np.log(row["count"] + 1) * 5 if row["category"] == "Global Hit" else 5

        top_titles = week_df[week_df["country_iso2"] == row["country_iso2"]]["show_title"].unique()[:5]
        top_titles_text = "<br>".join(top_titles) if len(top_titles) > 0 else "No data"

        popup_text = (
            f"{row['category']} ({selected_content})<br>"
            f"국가 코드: {row['country_iso2']}<br>"
            f"1위를 한 나라 수: {row['count']}<br>"
            f"Top 작품:<br>{top_titles_text}"
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color_map[row["category"]],
            fill=True,
            fill_color=color_map[row["category"]],
            fill_opacity=0.8,
            popup=popup_text,
        ).add_to(m)

colormap.add_to(m)

st_folium(m, width=800, height=500)

# 국가별 1위 작품 목록 표시
# st.write(f"### {selected_week} 주간 국가별 1위 작품 목록")
# st.dataframe(week_df[["country_name", "show_title", "category"]].drop_duplicates())

st.markdown("""
    <style>
    .stButton>button {
        background-color: #8A0829 !important;
        color: white !important;
        font-size: 16px;
        padding: 8px 14px;
        border-radius: 6px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #F7819F !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 홈 버튼 스타일 적용
st.markdown(
    """
    <style>
    .home-button-container button {
        background-color: #8A0829 !important;
        color: white !important;
        font-size: 16px;
        padding: 8px 14px;
        border-radius: 6px;
        border: none;
        transition: all 0.3s ease;
    }
    .home-button-container button:hover {
        background-color: #6A061F !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 중앙 정렬된 홈 버튼
home_col = st.columns([3, 2, 3])
with home_col[1]:
    # 버튼을 특정 div로 감싸서 스타일 적용
    st.markdown('<div class="home-button-container">', unsafe_allow_html=True)
    if st.button("🏠 Home", key="home"):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)