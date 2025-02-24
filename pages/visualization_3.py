import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2, venn3


# CSV 파일 로드 함수 (Streamlit 캐시 사용)
@st.cache_data
def load_data():
    netflix = pd.read_csv("data/Netflix_data.csv")
    amazon = pd.read_csv("data/Amazon_data.csv")
    apple = pd.read_csv("data/Apple_data.csv")
    hulu = pd.read_csv("data/Hulu_data.csv")
    return netflix, amazon, apple, hulu

def count_types(df, platform_name):
    """
    'type' 컬럼에서 movie, tv(=tv show) 개수를 세어 Series로 반환
    reindex(["movie", "tv"])로 순서를 고정하고, 값이 없으면 0으로 채움
    """
    return df['type'].value_counts().reindex(["movie", "tv"], fill_value=0).rename(platform_name)

def main():
    # 페이지 제목
    st.title("Movie & TV Show Distribution Across OTT Platforms")
    st.write("이 앱은 넷플릭스, 아마존 프라임, 애플 TV, 훌루에서 제공하는 영화/TV Show 개수를 시각화한 결과를 보여줍니다.")
    
    # 데이터 불러오기
    netflix, amazon, apple, hulu = load_data()

    # 플랫폼별 데이터 개수 정리 (행: movie/tv, 열: 각 플랫폼)
    data = pd.DataFrame({
        "Netflix": count_types(netflix, "Netflix"),
        "Amazon Prime": count_types(amazon, "Amazon Prime"),
        "Apple TV": count_types(apple, "Apple TV"),
        "Hulu": count_types(hulu, "Hulu")
    })
    
    # (중요) 열 순서를 재정의해서 'Amazon Prime'이 먼저 오도록 순서 변경
    # 원하는 순서: Amazon Prime → Netflix → Apple TV → Hulu
    data = data[["Amazon Prime", "Netflix", "Apple TV", "Hulu"]]
    
    # ---- 디자인 관련 설정 ----
    plt.style.use("seaborn-v0_8-whitegrid")  # 다른 스타일: 'ggplot', 'seaborn-ticks', 등등
    custom_colors = sns.color_palette("Set2", n_colors=2)  # 영화/TV에 사용할 2가지 색상
    
    fig, ax = plt.subplots(figsize=(10, 7))

    # 배경을 검은색으로 설정
    fig.patch.set_facecolor("#222222")
    ax.set_facecolor("#222222")

    # 누적 막대 그래프
    data.T.plot(
        kind="bar", 
        stacked=True, 
        color=custom_colors,
        ax=ax
    )

    # 축, 제목, 레이블 설정
    ax.set_xlabel("OTT Platform", fontsize=13, fontweight="bold", color="white")
    ax.set_ylabel("Number of Titles", fontsize=13, fontweight="bold", color="white")
    ax.set_title("Movie & TV Show Distribution Across OTT Platforms", fontsize=16, fontweight="bold", pad=20, color="white")
    ax.set_xticklabels(data.columns, rotation=0, fontsize=11, color="white")
    ax.legend(["Movie", "TV Show"], loc="upper right", fontsize=11, frameon=True)

    # 스파인(axes 경계선) 설정 (선택)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    # 각 막대에 라벨(개수, 퍼센트) 표시
    for container, content_type in zip(ax.containers, data.index):
        for i, bar in enumerate(container):
            height = bar.get_height()
            if height == 0:
                continue
            
            x_pos = bar.get_x() + bar.get_width() / 2
            y_pos = bar.get_y() + height / 2
            
            platform = data.columns[i]
            total = data[platform].sum()
            pct = (height / total) * 100
            
            label = f"{int(height)}\n({pct:.1f}%)"
            
            text_color = "white" if content_type == "movie" else "black"
            
            ax.text(
                x_pos, y_pos, label,
                ha="center", va="center",
                color=text_color,
                fontsize=10,
                fontweight="bold"
            )

    plt.tight_layout()

    # 스트림릿에 그래프 표시
    st.pyplot(fig)

if __name__ == "__main__":
    main()




import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
netflix_df = pd.read_csv("data/Netflix_data.csv")
amazon_df = pd.read_csv("data/Amazon_data.csv")
apple_df = pd.read_csv("data/Apple_data.csv")
hulu_df = pd.read_csv("data/Hulu_data.csv")

# 각 플랫폼별 장르 비율 계산 함수
def genre_ratio(df):
    genres = df['genres'].str.split(',', expand=True).stack().str.strip()  # 각 장르로 분리하고 공백 제거
    genre_counts = genres.value_counts()  # 장르별 개수 세기
    total_titles = len(df)  # 전체 영화/TV쇼 개수
    genre_percentage = (genre_counts / total_titles) * 100  # 각 장르의 비율 계산
    return genre_percentage.head(5)  # 상위 5개 장르만 반환

# 각 플랫폼별 상위 5개 장르 비율 계산
netflix_genre_ratio = genre_ratio(netflix_df)
amazon_genre_ratio = genre_ratio(amazon_df)
apple_genre_ratio = genre_ratio(apple_df)
hulu_genre_ratio = genre_ratio(hulu_df)

# 장르 이름을 고유한 색으로 매핑
genre_colors = {
    "Drama": "#FF9999",  
    "Comedy": "#66B3FF",  
    "Romance": "#99FF99",  
    "Documentary": "#FFCC99",  
    "Adventure": "#C2C2F0",  
    "Action": "#FFB3E6",  
    "Thriller": "#F0E68C",  
    "Crime": "#DDA0DD",  
    "Animation": "#8FBC8F",  
}

# Streamlit 앱 설정
st.title("📊 OTT 플랫폼 장르 비율 분석")
st.write("각 OTT 플랫폼별로 상위 5개 장르 비율을 시각화한 그래프입니다.")

# 상위 5개 장르 시각화 (파이 차트 사용)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 배경 색상 변경
fig.patch.set_facecolor('black')  # 전체 배경을 검은색으로 설정
for ax in axes.flat:
    ax.set_facecolor('black')  # 각 서브 플롯 배경을 검은색으로 설정
    ax.tick_params(axis='both', which='both', length=0, colors='white')  # 축의 색을 하얀색으로 설정

# 각 플랫폼별 상위 5개 장르 비율을 그래프에 표시
axes[0, 0].pie(netflix_genre_ratio, labels=netflix_genre_ratio.index, autopct='%1.1f%%', startangle=90, 
               colors=[genre_colors.get(x, "#FFFFFF") for x in netflix_genre_ratio.index], 
               textprops={'color': "white"})  
axes[0, 0].set_title("Netflix Top 5 Genre Distribution", color='white')

axes[0, 1].pie(amazon_genre_ratio, labels=amazon_genre_ratio.index, autopct='%1.1f%%', startangle=90, 
               colors=[genre_colors.get(x, "#FFFFFF") for x in amazon_genre_ratio.index], 
               textprops={'color': "white"})  
axes[0, 1].set_title("Amazon Prime Top 5 Genre Distribution", color='white')

axes[1, 0].pie(apple_genre_ratio, labels=apple_genre_ratio.index, autopct='%1.1f%%', startangle=90, 
               colors=[genre_colors.get(x, "#FFFFFF") for x in apple_genre_ratio.index], 
               textprops={'color': "white"})  
axes[1, 0].set_title("Apple TV Top 5 Genre Distribution", color='white')

axes[1, 1].pie(hulu_genre_ratio, labels=hulu_genre_ratio.index, autopct='%1.1f%%', startangle=90, 
               colors=[genre_colors.get(x, "#FFFFFF") for x in hulu_genre_ratio.index], 
               textprops={'color': "white"})  
axes[1, 1].set_title("Hulu Top 5 Genre Distribution", color='white')

# 레이아웃을 조정하여 그래프가 겹치지 않게 함
plt.tight_layout()

# Streamlit에 그래프 표시
st.pyplot(fig)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

# 데이터 로딩 함수
@st.cache_data
def load_data():
    """CSV 파일을 불러와서 DataFrame으로 반환"""
    # 각 플랫폼의 CSV 파일을 로드
    netflix_df = pd.read_csv("data/Netflix_data.csv")
    amazon_df = pd.read_csv("data/Amazon_data.csv")
    apple_df = pd.read_csv("data/Apple_data.csv")
    hulu_df = pd.read_csv("data/Hulu_data.csv")
    
    # 플랫폼 데이터 프레임을 딕셔너리로 반환
    platform_dict = {
        "Netflix": netflix_df,
        "Amazon Prime": amazon_df,
        "Apple TV": apple_df,
        "Hulu": hulu_df
    }
    return platform_dict

# ✅ 플랫폼 로고 파일 경로 지정
platform_logos = {
    "Netflix": "data/Netflix_logo.png",
    "Amazon Prime": "data/Amazon_logo.png",
    "Apple TV": "data/Apple_TV_logo.png",
    "Hulu": "data/Hulu_logo.png"
}


# 각 구역의 top 10을 뽑는 함수
def get_top10_from_subset(df, subset):
    """각 구역의 작품에 대해 IMDb 평균 평점 기준으로 상위 10개 작품을 반환"""
    subset_df = df[df['title'].isin(subset)]  # 해당 구역에 속한 작품들만 추출
    subset_df_sorted = subset_df.sort_values('imdbAverageRating', ascending=False)  # IMDb 평균 평점 기준으로 내림차순 정렬
    return subset_df_sorted[['title', 'imdbAverageRating']]  # 상위 작품 반환

def main():
    st.title("🎬 OTT 플랫폼 교집합 분석")

    # 데이터 불러오기
    platform_dict = load_data()

    # 플랫폼 선택 UI
    st.subheader("🔍 플랫폼 선택")
    col1, col2, col3, col4 = st.columns(4)

    selected_platforms = []

    for i, platform in enumerate(platform_dict.keys()):
        with [col1, col2, col3, col4][i]:
            selected = platform in selected_platforms
            checked = st.checkbox(f"{platform}", value=selected, key=f"chk_{platform}")
            if checked:
                selected_platforms.append(platform)
    # ✅ 플랫폼 로고 추가
            st.image(platform_logos[platform], width=100)
    if len(selected_platforms) < 2:
        st.warning("🚨 최소 2개 이상의 플랫폼을 선택해주세요.")
        return

    # 교집합 계산
    platform_sets = [set(platform_dict[platform]["title"]) for platform in selected_platforms]
    common_titles = platform_sets[0]
    for platform_set in platform_sets[1:]:
        common_titles = common_titles.intersection(platform_set)

    num_common_titles = len(common_titles)
    st.success(f"✅ **선택한 플랫폼** {selected_platforms} **에 모두 포함된 작품 개수**: {num_common_titles}")

    # 벤 다이어그램 그리기
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if len(selected_platforms) == 2:
        venn = venn2(platform_sets, selected_platforms, ax=ax)
            # 텍스트 스타일 조정
        for subset in venn.set_labels:
            if subset:
                subset.set_fontsize(14)
                subset.set_fontweight("bold")
                subset.set_color("white")

        for subset in venn.subset_labels:
            if subset:
                subset.set_fontsize(16)
                subset.set_fontweight("bold")
                subset.set_color("white")

        fig.patch.set_facecolor("#222222")  # 배경색
        ax.set_facecolor("#222222")  # 그래프 내부 배경색
        plt.title(" OTT Intersection ", fontsize=18, fontweight="bold", color="white")

        st.pyplot(fig)
        
    elif len(selected_platforms) == 3:
        venn = venn3(platform_sets, selected_platforms, ax=ax)
            # 텍스트 스타일 조정
        for subset in venn.set_labels:
            if subset:
                subset.set_fontsize(14)
                subset.set_fontweight("bold")
                subset.set_color("white")

        for subset in venn.subset_labels:
            if subset:
                subset.set_fontsize(16)
                subset.set_fontweight("bold")
                subset.set_color("white")

        fig.patch.set_facecolor("#222222")  # 배경색
        ax.set_facecolor("#222222")  # 그래프 내부 배경색
        plt.title(" OTT Intersection ", fontsize=18, fontweight="bold", color="white")

        st.pyplot(fig)
    elif len(selected_platforms) == 4:
        intersection = common_titles
        st.subheader("🏆집합별 IMDB TOP10")
        selected_zone = st.radio("구역을 선택하세요", ["Intersection"])

        if selected_zone == "Intersection":
            top10 = get_top10_from_subset(pd.concat([platform_dict[selected_platforms[0]], platform_dict[selected_platforms[1]],platform_dict[selected_platforms[2]],platform_dict[selected_platforms[3]]]), intersection)
        # 중복을 제거한 후, IMDb 평균 평점 기준으로 내림차순 정렬
        top10_unique = top10.drop_duplicates(subset="title").sort_values('imdbAverageRating', ascending=False)
        # 10개 작품만 선택
        top10 = top10_unique.head(10)
        st.write(top10)
    
    

    # 구역 선택 인터페이스
    if len(selected_platforms) == 2:
        # 2개 플랫폼 선택 시 3개 구역
        only_platform_1 = platform_sets[0] - platform_sets[1]
        only_platform_2 = platform_sets[1] - platform_sets[0]
        intersection = common_titles

        # 라디오 버튼을 사용하여 구역 선택
        st.subheader("🏆집합별 IMDB TOP10")
        selected_zone = st.radio("구역을 선택하세요", [f"Only {selected_platforms[0]}", f"Only {selected_platforms[1]}", "Intersection"])

        if selected_zone == f"Only {selected_platforms[0]}":
            top10 = get_top10_from_subset(platform_dict[selected_platforms[0]], only_platform_1)
        elif selected_zone == f"Only {selected_platforms[1]}":
            top10 = get_top10_from_subset(platform_dict[selected_platforms[1]], only_platform_2)
        else:
            top10 = get_top10_from_subset(pd.concat([platform_dict[selected_platforms[0]], platform_dict[selected_platforms[1]]]), intersection)
        # 중복을 제거한 후, IMDb 평균 평점 기준으로 내림차순 정렬
        top10_unique = top10.drop_duplicates(subset="title").sort_values('imdbAverageRating', ascending=False)
        # 10개 작품만 선택
        top10 = top10_unique.head(10)
        st.write(top10)

    elif len(selected_platforms) == 3:
        # 3개 플랫폼 선택 시 7개 구역
        only_platform_1 = platform_sets[0] - platform_sets[1] - platform_sets[2]
        only_platform_2 = platform_sets[1] - platform_sets[0] - platform_sets[2]
        only_platform_3 = platform_sets[2] - platform_sets[0] - platform_sets[1]

        platform_1_2 = platform_sets[0].intersection(platform_sets[1]) - platform_sets[2]
        platform_1_3 = platform_sets[0].intersection(platform_sets[2]) - platform_sets[1]
        platform_2_3 = platform_sets[1].intersection(platform_sets[2]) - platform_sets[0]

        intersection = common_titles

        # 라디오 버튼을 사용하여 구역 선택
        selected_zone = st.radio("구역을 선택하세요", [
            f"Only {selected_platforms[0]}",
            f"Only {selected_platforms[1]}",
            f"Only {selected_platforms[2]}",
            f"{selected_platforms[0]} & {selected_platforms[1]} Intersection",
            f"{selected_platforms[0]} & {selected_platforms[2]} Intersection",
            f"{selected_platforms[1]} & {selected_platforms[2]} Intersection",
            "Intersection"
        ])

        if selected_zone == f"Only {selected_platforms[0]}":
            top10 = get_top10_from_subset(platform_dict[selected_platforms[0]], only_platform_1)
        elif selected_zone == f"Only {selected_platforms[1]}":
            top10 = get_top10_from_subset(platform_dict[selected_platforms[1]], only_platform_2)
        elif selected_zone == f"Only {selected_platforms[2]}":
            top10 = get_top10_from_subset(platform_dict[selected_platforms[2]], only_platform_3)
        elif selected_zone == f"{selected_platforms[0]} & {selected_platforms[1]} Intersection":
            top10 = get_top10_from_subset(pd.concat([platform_dict[selected_platforms[0]], platform_dict[selected_platforms[1]]]), platform_1_2)
        elif selected_zone == f"{selected_platforms[0]} & {selected_platforms[2]} Intersection":
            top10 = get_top10_from_subset(pd.concat([platform_dict[selected_platforms[0]], platform_dict[selected_platforms[2]]]), platform_1_3)
        elif selected_zone == f"{selected_platforms[1]} & {selected_platforms[2]} Intersection":
            top10 = get_top10_from_subset(pd.concat([platform_dict[selected_platforms[1]], platform_dict[selected_platforms[2]]]), platform_2_3)
        else:
            top10 = get_top10_from_subset(pd.concat([platform_dict[selected_platforms[0]], platform_dict[selected_platforms[1]], platform_dict[selected_platforms[2]]]), intersection)
        # 중복을 제거한 후, IMDb 평균 평점 기준으로 내림차순 정렬
        top10_unique = top10.drop_duplicates(subset="title").sort_values('imdbAverageRating', ascending=False)
        # 10개 작품만 선택
        top10 = top10_unique.head(10)
        st.write(top10)
    

if __name__ == "__main__":
    main()


# 🏠 홈으로 가는 버튼
home_col = st.columns([3, 2, 3])  # 중앙 정렬
with home_col[1]:
    if st.button("🏠 Home", key="home"):
        st.switch_page("app.py")  # 홈으로 이동