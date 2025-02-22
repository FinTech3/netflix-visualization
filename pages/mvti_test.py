import requests
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MVTI 영화 성향 테스트", layout="wide")
st.title("MVTI")
st.write("내 성향으로 나만의 영화 추천받기")

# API 키 설정
api_key = '9ffc1ec82777dd0129dab4d5e890e96b'

# 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return pd.read_csv(os.path.join(base_path, "1-1_data.csv"))

# 📌 CSS 추가: 질문 박스 스타일 적용
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

    .question-box {
        background-color: rgba(138, 8, 41, 0.8);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        width: 80%;
        margin: 20px auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 📌 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# 📌 질문 리스트 (각 질문별 선택지와 키워드 매핑)
questions = [
    {
        "question": "문득 하늘을 바라보았는데, 갑자기 어떤 감정이 차올랐어. 어떤 감정일까?",
        "options": {
            "A. 노을을 보고 센티멘털한 감성에 잠겼어": ["sentimental", "melancholy", "nostalgic","romance"],
            "B. 왠지 희망적이고 행복한 감정이 들었어": ["hopeful", "happy", "uplifting"],
            "C. 구름 낀 하늘처럼 갑갑하고 답답한 마음이 들었어": ["gloomy", "tense", "serious"],
            "D. 특별한 감흥 없이 심심하고 무료하게 느껴졌어": ["neutral", "calm", "boring"]
        }
    },
    {
        "question": "자, 이제 여행지를 골라보자. 어디로 가볼까?",
        "options": {
            "A. 아시아 지역 여행": ["Asia", "adventure", "culture"],
            "B. 미국과 북미 여행": ["America", "modern", "urban"],
            "C. 유럽 여행": ["Europe", "romantic", "history"],
            "D. 동네 여행": ["local", "comfort", "slice of life"]
        }
    },
    {
        "question": "설레는 여행의 시작, 길을 걷다가 바스락 거리는 소리가 들려서 보았더니!",
        "options": {
            "A. 작은 강아지가 나를 빼꼼 보고 있네": ["dog", "animal", "pet"],
            "B. 어린 아이가 무언가를 찾고 있었어": ["kid", "child", "innocence"],
            "C. 배낭 멘 여행자가 물을 마시고 있었어": ["travel", "journey", "discovery"],
            "D. 의심스러운 분위기의 첩보요원 같은 사람이 숨어 있었어": ["spy", "mystery", "action"]
        }
    },
    {
        "question": "큰 광장에 가보니 사람들이 잔뜩 모여 북적이고 있었는데…",
        "options": {
            "A. 교복을 입은 학생들이 한데 모여 놀고 있었어": ["students", "friendship", "school"],
            "B. 서커스 단의 마술사가 선사하는 마술을 보는 사람들이 있었어": ["circus", "magic", "performance"],
            "C. 경찰들이 주변을 통제하며 경계 태세를 갖추고 있었어": ["police", "crime", "thriller"],
            "D. 시위대가 막 시위를 벌이고 구호를 외치고 있었어": ["protest", "revolution", "justice"]
        }
    }
]

# 📌 현재 페이지 질문 표시
current_page = st.session_state.page
if current_page <= len(questions):
    q_data = questions[current_page - 1]

    # 📌 질문과 선택지를 하나의 박스 안에 넣기 (HTML + CSS 적용)
    st.markdown(f"""
        <div class="question-box">
            <h3>Q{current_page}. {q_data['question']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # 📌 선택지 박스 (st.radio()를 같은 컨테이너 안에서 표시)
    with st.container():
        options = list(q_data["options"].keys())
        selected_option = st.radio("선택하세요:", options, key=f"q{current_page}")

    # 📌 다음 페이지 버튼
    if st.button("다음", key=f"next{current_page}"):
        st.session_state.answers[f"Q{current_page}"] = selected_option
        # 선택한 키워드를 저장
        selected_keywords = q_data["options"][selected_option]
        st.session_state.selected_keywords.extend(selected_keywords)
        st.session_state.page += 1
        st.rerun()

# 📌 결과 페이지
else:
    # st.title("📊 결과 페이지")
    # st.write("✨ 당신의 영화 성향 테스트 결과 ✨")
    # st.write("당신이 선택한 답변")

    # for q_num, answer in st.session_state.answers.items():
    #     st.markdown(f"**{q_num}**: {answer}")

    # # 선택한 키워드 출력
    # st.markdown("""
    #     <div class="question-box">
    #         <h3>📌 추천 키워드</h3>
    #     </div>
    # """, unsafe_allow_html=True)
    
    # keyword_list = ", ".join(set(st.session_state.selected_keywords))
    # st.write(f"🎬 당신의 영화 추천 키워드: {keyword_list}")

    # # 홈으로 돌아가기 버튼
    # if st.button("🏠 다시 테스트하기"):
    #     st.session_state.page = 1
    #     st.session_state.answers = {}
    #     st.session_state.selected_keywords = []
    #     st.rerun()
    df = load_data()

    # st.write("📌 데이터프레임 컬럼 확인:", df.columns.tolist())


    # ✅ NaN 처리 (keywords가 없는 경우 빈 문자열로 대체)
    df["keywords"] = df["keywords"].fillna("")

    # ✅ 키워드 매칭 개수 계산 함수
    def count_keyword_matches(row):
        movie_tags = row["keywords"].split(", ")  # 태그를 리스트로 변환
        return sum(tag in st.session_state.selected_keywords for tag in movie_tags)  # 키워드 매칭 개수 카운트

    # ✅ 각 영화에 대해 매칭된 키워드 개수를 추가
    df["match_count"] = df.apply(count_keyword_matches, axis=1)

    # ✅ 매칭 개수가 많은 순으로 정렬 후 상위 5개 영화만 선택
    df_sorted = df.sort_values(by="match_count", ascending=False).head(5)

    # ✅ 결과 출력 (매칭 개수가 1개 이상인 영화만 표시)
    df_filtered = df_sorted[df_sorted["match_count"] > 0]

    # ✅ Streamlit에서 결과 출력
    st.title("🎬 Netflix 추천 컨텐츠 (TOP 5)")
    #st.dataframe(df_sorted[["show_title","category", "weekly_rank", "weekly_views", "keywords", "match_count"]])


    # ✅ 영화 상세 정보 및 포스터 가져오기
    for index, row in df_sorted.iterrows():
        movie_title = row["show_title"]
        category = row["category"]
    
        # 카테고리에 따라 API URL 결정
        if category.startswith("Films"):
            search_url = "https://api.themoviedb.org/3/search/movie"
        elif category.startswith("TV"):
            search_url = "https://api.themoviedb.org/3/search/tv"
        else:
            st.write(f"Unknown category for {movie_title}: {category}")
            continue

        # 영화 검색
        params = {
            'api_key': api_key,
            'query': movie_title,
            'language': 'ko'
        }
        response = requests.get(search_url, params=params)
        results = response.json().get('results', [])

        if results:
            movie_id = results[0]['id']
            
            # 영화 상세 정보 가져오기
            details_url = f"https://api.themoviedb.org/3/{'movie' if 'movie' in search_url else 'tv'}/{movie_id}"
            details_params = {
                'api_key': api_key,
                'language': 'ko-KR'
            }
            details_response = requests.get(details_url, params=details_params)
            movie_details = details_response.json()
            print(movie_details)
            
            # 영화 정보 표시 (한 줄 정렬)
            col1, col2 = st.columns([1, 3.5])
            with col1:
                poster_path = movie_details.get('poster_path')
                if poster_path:
                    poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
                    st.image(poster_url, caption=movie_title, use_container_width=True)
                else:
                    st.write(f"{movie_title}: 포스터를 찾을 수 없습니다.")
            
            with col2:
                st.subheader(movie_title)
                st.write(f"**개봉일:** {movie_details.get('release_date', '정보 없음')}")
                st.write(f"**평점:** {movie_details.get('vote_average', '정보 없음')}")
                st.write(f"**줄거리:** {movie_details.get('overview', '줄거리 정보가 없습니다.')}")
        else:
            st.write(f"{movie_title}: 영화 정보를 찾을 수 없습니다.")



# 🏠 홈으로 가는 버튼 (중앙 정렬)
home_col = st.columns([3, 2, 3])
with home_col[1]:
    if st.button("🏠 Home", key="home"):
        st.switch_page("app.py")  # 홈으로 이동
