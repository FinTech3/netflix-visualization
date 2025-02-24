import streamlit as st
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Keyword WordCloud", layout="wide")
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

def clean_keyword(keyword):
    keyword = keyword.lower().strip()
    keyword = re.sub(r"\s+", " ", keyword)
    keyword = re.sub(r"[^a-z0-9 ]", "", keyword)
    return keyword

def load_keywords():
    keyword_df = pd.read_csv("data/keyword_counts.csv")
    return keyword_df["keyword"].tolist()

def load_movies():
    return pd.read_csv("data/2025-02-12_global_alltime_filtered_v2.csv")

def generate_wordcloud(keyword_counts):
    wordcloud = WordCloud(width=800, height=400, background_color="black", colormap="Reds", max_words=100).generate_from_frequencies(keyword_counts)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor('black')
    return fig

keywords = load_keywords()
movies_df = load_movies()

def main():
    if "selected_keyword" not in st.session_state:
        st.session_state["selected_keyword"] = None
    if st.session_state["selected_keyword"] is None:
        show_wordcloud()
    else:
        show_filtered_movies()

def show_wordcloud():
    st.markdown('<div class="title">Netflix Keyword WordCloud</div>', unsafe_allow_html=True)
    keyword_counts = pd.read_csv("./data/keyword_counts.csv").set_index("keyword")["count"].to_dict()
    fig = generate_wordcloud(keyword_counts)
    st.pyplot(fig)
    st.markdown('<h3 style="color: #A9A9A9;">🎯 Select Your Keyword</h3>', unsafe_allow_html=True)
    selected_keyword = st.selectbox("", keywords, index=None, placeholder="Choose a keyword...")
    if selected_keyword:
        st.session_state["selected_keyword"] = selected_keyword
        st.rerun()

def display_movie_list(filtered_movies):
    st.markdown('<h2 style="color: #D3D3D3;">📽️ 관련 영화 리스트</h2>', unsafe_allow_html=True)
    movies_to_display = filtered_movies[:5] if len(filtered_movies) > 5 else filtered_movies
    for _, row in movies_to_display.iterrows():
        row_cols = st.columns([1, 3])
        with row_cols[0]:
            if pd.notna(row.get("title_image_url")):
                st.markdown(
                    f'<img src="{row["title_image_url"]}" style="border-radius:15px; width:300px; margin-bottom:20px;" alt="Movie Image">',
                    unsafe_allow_html=True
                )
        with row_cols[1]:
            st.markdown(f"<h3 style='color: #831010;'>🎬 {row['show_title']}</h3>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <p style="font-size:16px; color:white; margin:0;">
                    <strong>Week:</strong> {row['week']}<br>
                    <strong>Category:</strong> {row['category']}<br>
                    <strong>Rank:</strong> {row['weekly_rank']}<br>
                    <strong>Views:</strong> {row['weekly_views']:,}<br>
                    <strong>Keywords:</strong> <span style="white-space: normal; word-wrap: break-word;">{', '.join(row['keywords'].split(', ')[:3])}</span>
                </p>
                """, unsafe_allow_html=True)
        st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        keyword_list = row['keywords'].split(', ')[:3]
        if keyword_list:
            btn_cols = st.columns(len(keyword_list))
            for i, keyword in enumerate(keyword_list):
                if keyword in keywords:
                    if btn_cols[i].button(keyword, key=f"{row['show_title']}_{keyword}_{i}", use_container_width=True):
                        st.session_state["selected_keyword"] = keyword
                        st.rerun()
                else:
                    btn_cols[i].write(keyword)
        st.markdown("<hr>", unsafe_allow_html=True)

def show_filtered_movies():
    selected_keyword = st.session_state["selected_keyword"]
    st.markdown(f'<div class="title">Movies Related to: {selected_keyword}</div>', unsafe_allow_html=True)
    filtered_movies = movies_df[movies_df["keywords"].apply(lambda x: any(clean_keyword(selected_keyword) in clean_keyword(k) for k in str(x).split(",")))]
    if filtered_movies.empty:
        st.warning("⚠️ No movies found for the selected keyword.")
    else:
        display_movie_list(filtered_movies)
    if st.button("⬅️ Back to Keyword Selection"):
        st.session_state["selected_keyword"] = None
        st.rerun()
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #4A4A4A;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    home_col = st.columns([3, 2, 3])
    with home_col[1]:
        st.markdown(
            """
            <style>
            .home-button-container button {
                background-color: white !important;
                color: #8A0829 !important;
                font-size: 16px;
                padding: 8px 14px;
                border-radius: 6px;
                border: none;
                transition: all 0.3s ease;
            }
            .home-button-container button:hover {
                background-color: #E0E0E0 !important;
            }
            .home-button-container button:focus {
                color: #8A0829 !important;
                outline: none !important;
                box-shadow: none !important;
            }
            </style>
            <div class="home-button-container">
            """, unsafe_allow_html=True)
        if st.button("🏠 Home", key="home"):
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

