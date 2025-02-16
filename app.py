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
        width: 60%;  /* 중앙 정렬을 위해 동일한 너비 적용 */
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

    .stButton>button {
        background-color: #8A0829 !important; /* 진한 와인색 */
        color: white !important;
        font-size: 16px;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #F7819F !important; /* 밝은 핑크 */
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 제목 및 설명
st.markdown('<p class="title">Netflix Is All You Need</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the world through data</p>', unsafe_allow_html=True)

# ✅ MVTI 테스트 박스 (컨테이너 내부에 버튼 포함)
with st.container():
    st.markdown("""
        <div class="container">
            <h2>Discover Your Travel Personality</h2>
            <p>Take our MVTI test and uncover your ideal travel experiences.</p>
        </div>
    """, unsafe_allow_html=True)

    # 👉 중앙 정렬을 위해 `st.columns([1,3,1])` 사용
    mvti_col1, mvti_col2, mvti_col3 = st.columns([1, 3, 1])
    with mvti_col2:  # 중간 컬럼에 배치하여 중앙 정렬
        if st.button("Start MVTI Test →", key="mvti"):
            st.switch_page("pages/mvti_test.py")  # 🚀 현재 페이지에서 이동

# ✅ 버튼 그리드 레이아웃 (MVTI 컨테이너와 너비 맞추기)
st.markdown("<br><br>", unsafe_allow_html=True)  # 버튼과 MVTI 테스트 간 간격 추가

# 👉 MVTI 컨테이너 너비와 맞추기 위해 동일한 컬럼 비율 적용
btn_col1, btn_col2, btn_col3 = st.columns([1, 3, 1])  

with btn_col2:  # 중앙 컬럼에 버튼 배치하여 정렬 맞춤
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 주가", key="stock"):
            st.switch_page("pages/visualization_1.py")

    with col2:
        if st.button("🌎 국가", key="country"):
            st.switch_page("pages/visualization_2.py")

    with col3:
        if st.button("▶️ OTT", key="ott"):
            st.switch_page("pages/visualization_3.py")

    col4, col5 = st.columns(2)

    with col4:
        if st.button("🏷️ 태그", key="tag"):
            st.switch_page("pages/visualization_4.py")

    with col5:
        if st.button("🏆 수상", key="award"):
            st.switch_page("pages/visualization_5.py")
