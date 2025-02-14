import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# Streamlit 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# 넷플릭스 주가 vs 글로벌 1위 작품 시각화 함수
def show_stock_vs_top_movie():
    st.subheader("📈 넷플릭스 주가 vs 글로벌 1위 작품")

    # 넷플릭스 주가 데이터 가져오기
    stock_data = yf.download("NFLX", start="2020-01-01", end=datetime.date.today().strftime('%Y-%m-%d'))
    stock_data = stock_data[['Close']]
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['Week'] = stock_data['Date'].dt.to_period('W').apply(lambda r: r.start_time)  # 주 단위 변환

    # 1위 작품 데이터 불러오기
    movie_data = pd.read_csv("./2-2_movies.csv")
    movie_data['Week'] = pd.to_datetime(movie_data['week'])  # 'week' 칼럼을 datetime으로 변환
    
    # 주가 데이터와 영화 데이터를 주 단위로 병합
    merged_data = pd.merge(stock_data, movie_data, on='Week', how='left')
    
    # 주가 그래프 그리기
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(merged_data['Date'], merged_data['Close'], color='#E50914', label='Netflix Stock Price')
    
    # 특정 기간의 1위 영화 표시
    for _, row in merged_data.iterrows():
        if pd.notna(row['Title']):
            ax.annotate(row['Title'], xy=(row['Date'], row['Close']),
                        xytext=(row['Date'], row['Close'] + 20),
                        arrowprops=dict(facecolor='white', shrink=0.05),
                        color='white', fontsize=10, ha='center')
    
    ax.set_title("Netflix Stock Price vs Global Top 1 Movie", fontsize=14, color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Stock Price (USD)", color='white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(colors='white')
    ax.legend()
    
    st.pyplot(fig)

# 메인 페이지 함수
def main():
    # 웹 페이지 기본 설정
    st.set_page_config(page_title="Netflix Is All You Need", page_icon="🎬", layout="wide")
    
    # 스타일 적용
    st.markdown(
        """
        <style>
        body { background-color: black; color: white; }
        .title { text-align: center; font-size: 50px; font-weight: bold; color: #E50914; }
        .button-container { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
        .stButton>button {
            background-color: #564d4d !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: bold !important;
            border: 2px solid #8c8c8c !important;
            border-radius: 10px !important;
            padding: 15px 30px !important;
            width: 100% !important;
        }
        .center-button {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            margin-top: 50px;
        }
        .center-button button {
            font-size: 30px !important;
            padding: 30px 60px !important;
            width: 60% !important;
            background-color: #E50914 !important;
            border: 2px solid #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 현재 페이지 확인 후 화면 렌더링
    if st.session_state["page"] == "home":
        # 제목 출력
        st.markdown('<div class="title">Netflix Is All You Need</div>', unsafe_allow_html=True)

        # 중앙에 MVTI 추천 시스템 버튼
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("🎭 MVTI - 넷플릭스 컨텐츠 추천받기", key="mvti", help="나에게 맞는 넷플릭스 콘텐츠를 추천받아 보세요."):
            pass
        st.markdown('</div>', unsafe_allow_html=True)

        # 버튼 리스트 (4개 버튼 + 하단 핀테크 특집 콘텐츠)
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📈 넷플릭스 주가 vs 글로벌 1위 작품"):
                st.session_state["page"] = "stock_vs_movie"
                st.rerun()  # 페이지 새로고침하여 해당 페이지 표시
        with col2:
            if st.button("🎥 타 OTT 비교: 독점 vs 비독점"):
                pass
        with col3:
            if st.button("🔍 키워드 기반 추천 (워드 클라우드)"):
                pass
        with col4:
            if st.button("🏆 역대 영화제 수상 인물 추천"):
                pass
        st.markdown('</div>', unsafe_allow_html=True)

        # 핀테크 특집 콘텐츠 버튼 (하단에 병합된 열)
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("💰 핀테크 특집 콘텐츠"):
            pass
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state["page"] == "stock_vs_movie":
        show_stock_vs_top_movie()

# 앱 실행
if __name__ == "__main__":
    main()
