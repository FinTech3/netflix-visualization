import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Netflix Is All You Need", layout="wide")

# ✅ 스타일 적용
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
        margin-bottom: 10px !important;
    }
    
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }

    .container {
        background-color: rgba(138, 8, 41, 0.8);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        width: 60%;
        margin: 0 auto 20px auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .container h2 {
        color: white;
        font-size: 28px;
        margin-bottom: 10px;
    }

    .container p {
        color: white;
        font-size: 18px;
        margin-bottom: 15px;
    }

    .stButton>button {
        background-color: #8A0829 !important;
        color: white !important;
        font-size: 20px !important;
        padding: 24px 45px;
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

# 제목 및 설명
st.markdown('<p class="title">Netflix Is All You Need</p>', unsafe_allow_html=True)

# ✅ MVTI 테스트 박스 (컨테이너 내부에 버튼 포함)
with st.container():
    st.markdown("""
        <div class="container">
            <h2>Discover Your Streaming Personality</h2>
            <p>Take our MVTI test and find your perfect Netflix match!</p>
        </div>
    """, unsafe_allow_html=True)

    # 👉 버튼을 컨테이너 안에서 중앙 정렬
    mvti_col1, mvti_col2, mvti_col3 = st.columns([3, 2, 3])  # 가운데 컬럼을 키움
    with mvti_col2:
        if st.button("Start MVTI Test →", key="mvti"):
            st.switch_page("pages/mvti_test.py")

# ✅ 버튼 레이아웃 조정 (버튼 간 간격 줄이기)
btn_col = st.columns(5)  # 버튼을 한 줄에 최대한 배치

with btn_col[0]:
    if st.button("📈 주가", key="stock"):
        st.switch_page("pages/visualization_1.py")

with btn_col[1]:
    if st.button("🌎 국가", key="country"):
        st.switch_page("pages/visualization_2.py")

with btn_col[2]:
    if st.button("▶️ OTT", key="ott"):
        st.switch_page("pages/visualization_3.py")

with btn_col[3]:
    if st.button("🏷️ 태그", key="tag"):
        st.switch_page("pages/visualization_4.py")

with btn_col[4]:
    if st.button("🏆 수상", key="award"):
        st.switch_page("pages/visualization_5.py")
