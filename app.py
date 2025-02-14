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
        font-size: 60px !important;
        font-weight: bold !important;
        text-align: center !important;
        color: white !important;
        margin-bottom: 20px !important;
    }
    
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
    }

    .container {
        background-color: rgba(138, 8, 41, 0.8);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        width: 60%;
        margin: 0 auto 40px auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .container h2 {
        color: white;
        font-size: 28px;
        margin-bottom: 15px;
    }

    .container p {
        color: white;
        font-size: 18px;
        margin-bottom: 20px;
    }

    .button-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }

    .button {
        width: calc(33% - 20px);
        padding: 15px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        background: rgba(138, 8, 41, 0.8);
        color: white !important;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .button:hover {
        background: #F7819F;
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .mvti-button {
        background: #F7819F;
        color: white !important;
        padding: 15px 30px;
        font-size: 20px;
        margin-top: 20px;
    }

    .mvti-button:hover {
        background: #8A0829;
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
                '<a href="/pages/mvti_test" class="button mvti-button">Start MVTI Test →</a>'
                '</div>', unsafe_allow_html=True)

# 버튼 그리드 레이아웃
st.markdown('<div class="button-grid">'
            '<a href="/pages/visualization_1.py" class="button">📈 주가</a>'
            '<a href="/pages/visualization_2.py" class="button">🌎 국가</a>'
            '<a href="/pages/visualization_3.py" class="button">▶️ OTT</a>'
            '<a href="/pages/visualization_4.py" class="button">🏷️ 태그</a>'
            '<a href="/pages/visualization_5.py" class="button">🏆 수상</a>'
            '</div>', unsafe_allow_html=True)