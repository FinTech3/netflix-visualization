import streamlit as st
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ✅ Streamlit 설정 (최상단에 위치해야 함)
st.set_page_config(page_title="Netflix Keyword WordCloud", layout="wide")

# 스타일 적용 (배경을 검은색, 타이틀 색상 흰색으로 설정)
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: white;
    }
    .stSelectbox>div[data-baseweb="select"] {
        background-color: #4a4a4a !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 키워드 정제 함수
def clean_keyword(keyword):
    keyword = keyword.lower().strip()
    keyword = re.sub(r"\s+", " ", keyword)  # 다중 공백 제거
    keyword = re.sub(r"[^a-z0-9 ]", "", keyword)  # 특수문자 제거
    return keyword

# CSV 파일에서 키워드 데이터 로드
def load_keywords():
    keyword_df = pd.read_csv("./data/keyword_counts.csv")
    return keyword_df["keyword"].tolist()

# CSV 파일에서 영화 데이터 로드
def load_movies():
    return pd.read_csv("./data/2025-02-12_global_alltime_filtered_v2.csv")

# 워드클라우드 생성 함수
def generate_wordcloud(keyword_counts):
    wordcloud = WordCloud(
        width=800, height=400,
        background_color="black", colormap="Reds",
        max_words=100
    ).generate_from_frequencies(keyword_counts)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor('black')
    return fig

# 키워드 목록 및 영화 데이터 로드
keywords = load_keywords()
movies_df = load_movies()

# 페이지 상태 확인
def main():
    if "selected_keyword" not in st.session_state:
        st.session_state["selected_keyword"] = None

    if st.session_state["selected_keyword"] is None:
        show_wordcloud()
    else:
        show_filtered_movies()

# 워드클라우드 및 키워드 선택 페이지
def show_wordcloud():
    st.markdown('<div class="title">Netflix Keyword WordCloud</div>', unsafe_allow_html=True)
    
    # 워드클라우드 생성 및 시각화
    keyword_counts = pd.read_csv("./data/keyword_counts.csv").set_index("keyword")["count"].to_dict()
    fig = generate_wordcloud(keyword_counts)
    st.pyplot(fig)
    
    # 키워드 선택
    st.markdown('<h3 style="color: #A9A9A9;">🎯 Select Your Keyword</h3>', unsafe_allow_html=True)
    selected_keyword = st.selectbox("", keywords, index=None, placeholder="Choose a keyword...")
    
    if selected_keyword:
        st.session_state["selected_keyword"] = selected_keyword
        st.rerun()

# 🎨 필터링된 영화 리스트를 텍스트 형식으로 출력하는 함수
def display_movie_list(filtered_movies):
    st.markdown('<h2 style="color: #D3D3D3;">📽️ 관련 영화 리스트</h2>', unsafe_allow_html=True)

    movies_to_display = filtered_movies[:5] if len(filtered_movies) > 5 else filtered_movies

    for _, row in movies_to_display.iterrows():
        keywords_list = row['keywords'].split(', ')[:3]

        with st.container():
            st.markdown(f"<h3 style='color: #831010;'>🎬 {row['show_title']}</h3>", unsafe_allow_html=True)

            st.write(f"**Week:** {row['week']}  \n"
                     f"**Category:** {row['category']}  \n"
                     f"**Rank:** {row['weekly_rank']}  \n"
                     f"**Views:** {row['weekly_views']:,}  \n"
                     f"**Keywords:** {', '.join(keywords_list)}", unsafe_allow_html=True)

            # 키워드 버튼 표시
            cols = st.columns(len(keywords_list))
            for i, keyword in enumerate(keywords_list):
                if keyword in keywords:
                    if cols[i].button(keyword, key=f"{row['show_title']}_{keyword}_{i}", use_container_width=True):
                        st.session_state["selected_keyword"] = keyword
                        st.rerun()
                else:
                    cols[i].write(keyword)

            st.divider()

# 필터링된 영화 리스트 페이지
def show_filtered_movies():
    selected_keyword = st.session_state["selected_keyword"]
    st.markdown(f'<div class="title">Movies Related to: {selected_keyword}</div>', unsafe_allow_html=True)
    
    # 영화 키워드 정제 후 필터링
    filtered_movies = movies_df[movies_df["keywords"].apply(lambda x: any(clean_keyword(selected_keyword) in clean_keyword(k) for k in str(x).split(",")))]
    

    if filtered_movies.empty:
        st.warning("⚠️ No movies found for the selected keyword.")
    else:
        display_movie_list(filtered_movies)

    # 뒤로 가기 버튼
    if st.button("⬅️ Back to Keyword Selection"):
        st.session_state["selected_keyword"] = None
        st.rerun()

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #4A4A4A;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()