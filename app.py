import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Netflix Is All You Need", layout="wide")

# 스타일 적용
st.markdown("""
    <style>
        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: grey;
        }
        .container {
            background-color: black;
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .button-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        .button {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# 제목 및 설명
st.markdown('<p class="title">Netflix Is All You Need</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the world through data</p>', unsafe_allow_html=True)

# MVTI 테스트 박스
with st.container():
    st.markdown('<div class="container"><h2>Discover Your Travel Personality</h2>'
                '<p>Take our MVTI test and uncover your ideal travel experiences.</p>'
                '<a href="/pages/mvti_test" class="button" style="background:white; color:black; padding:10px; border-radius:5px; text-decoration:none;">Start MVTI Test →</a>'
                '</div>', unsafe_allow_html=True)

# 버튼 레이아웃
col1, col2 = st.columns(2)

# 첫 번째 컬럼 버튼
with col1:
    if st.button("📈 주가"):
        st.switch_page("pages/visualization_1.py")
    if st.button("🌎 국가"):
        st.switch_page("pages/visualization_2.py")
    if st.button("▶️ OTT"):
        st.switch_page("pages/visualization_3.py")

# 두 번째 컬럼 버튼
with col2:
    if st.button("🏷️ 태그"):
        st.switch_page("pages/visualization_4.py")
    if st.button("🏆 수상"):
        st.switch_page("pages/visualization_5.py")
    if st.button("💳 핀테크"):
        st.switch_page("pages/visualization_6.py")
