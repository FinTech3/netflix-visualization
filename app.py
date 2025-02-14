import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Netflix Is All You Need", layout="wide")

# 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://github.com/user-attachments/assets/585ecfa1-c4fd-4d92-a451-cac484a05c78");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    
    .title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: white;
    }
    
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: white;
    }

    .container {
        background-color: #8A0829;
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        width: 40%;
        margin: auto;
    }

    .container h2, .container p {
        color: white;
    }

    .button-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 20px;
    }

    /* 기본 버튼 스타일 */
    .button {
        width: 30%;
        padding: 15px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        background: #8A0829; 
        color: white !important; /* 글자 색상을 흰색으로 강제 */
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
        transition: background 0.3s ease, color 0.3s ease;
    }

    /* 버튼 호버 효과 */
    .button:hover {
        background: #F7819F; /* 호버 시 더 밝은 색 */
        color: white !important;
    }

    /* 버튼 컨테이너 */
    .button-container {
        text-align: center;
        margin: 10px 0;
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
                '<a href="/pages/mvti_test" class="button">Start MVTI Test →</a>'
                '</div>', unsafe_allow_html=True)

# 버튼 레이아웃 (HTML 버튼 활용)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="button-container"><a href="/pages/visualization_1.py" class="button">📈 주가</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="button-container"><a href="/pages/visualization_2.py" class="button">🌎 국가</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="button-container"><a href="/pages/visualization_3.py" class="button">▶️ OTT</a></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="button-container"><a href="/pages/visualization_4.py" class="button">🏷️ 태그</a></div>', unsafe_allow_html=True)
    st.markdown('<div class="button-container"><a href="/pages/visualization_5.py" class="button">🏆 수상</a></div>', unsafe_allow_html=True)
