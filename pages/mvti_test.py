import streamlit as st

st.set_page_config(page_title="MVTI 영화 성향 테스트", layout="wide")
st.title("MVTI")
st.write("내 성향으로 나만의 영화 추천받기")

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
    </style>
""", unsafe_allow_html=True)

# 🏠 홈으로 가는 버튼
home_col = st.columns([3, 2, 3])  # 중앙 정렬
with home_col[1]:
    if st.button("🏠 Home", key="home"):
        st.switch_page("app.py")  # 홈으로 이동