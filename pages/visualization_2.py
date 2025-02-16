import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 데이터 로드 함수 (경로 수정)
@st.cache_data
def load_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    movies_path = os.path.join(base_path, "2-2_movies.csv")
    series_path = os.path.join(base_path, "2-2_tv.csv")

    movies_df = pd.read_csv(movies_path)  # 영화 데이터
    series_df = pd.read_csv(series_path)  # 시리즈 데이터
    return movies_df, series_df

movies_df, series_df = load_data()

# 데이터 전처리 (주간 1위만 필터링)
movies_top1 = movies_df[movies_df["weekly_rank"] == 1]
series_top1 = series_df[series_df["weekly_rank"] == 1]

# 영화와 시리즈 데이터 합치기
top1_df = pd.concat([movies_top1, series_top1], ignore_index=True)

# 국가별 1위 작품 개수 계산
country_counts = top1_df.groupby("show_title")["country_iso2"].nunique()

# 글로벌 1위(2개 이상 국가에서 1위)와 국가별 희귀 1위(1개 국가만 1위) 구분
top1_df["category"] = top1_df["show_title"].map(lambda x: "Global Hit" if country_counts[x] > 1 else "National Hit")

# Streamlit UI
st.title("Netflix Top 1 Visualization")
st.write("각 국가에서 1위를 차지한 작품을 글로벌/국가별 히트로 나누어 시각화합니다.")

# 지도 시각화
fig = px.scatter_geo(
    top1_df,
    locations="country_iso2",
    hover_name="show_title",
    color="category",
    projection="natural earth",
    title="Netflix Top 1 Hits: National vs Global",
    size_max=20,
    template="plotly_dark"
)

st.plotly_chart(fig)

# 국가별 1위 작품 목록 표시
st.write("### 국가별 1위 작품 목록")
st.dataframe(top1_df[["country_name", "show_title", "category"]].drop_duplicates())
