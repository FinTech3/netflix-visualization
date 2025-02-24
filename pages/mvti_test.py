import requests
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MVTI 영화 성향 테스트", layout="wide")
st.header("MVTI 영화 성향 테스트")

# API 키 설정
api_key = '9ffc1ec82777dd0129dab4d5e890e96b'

# 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return pd.read_csv(os.path.join(base_path, "1-1_data.csv"))

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

    .question-box {
        background: #F5F5F5;  /* 박스 배경색 (연한 핑크) */
        padding: 25px;  /* 박스 내부 여백 (패딩) */
        border-radius: 15px;  /* 박스 모서리를 둥글게 (둥근 정도: 15px) */
        color: white !important;  /* 텍스트 색상 (흰색) */
        text-align: center ;  /* 텍스트 중앙 정렬 */
        width: 70%;  /* 박스 너비를 화면의 80%로 설정 */
        margin: 20px 0 20px 0;  /* 위/아래 마진 20px, 좌우 마진 없음 */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);  /* 박스 그림자 효과 */
        font-size: 14px;  /* 글자 크기 (14px) */
        font-weight: bold;  /* 글자 굵기 (굵게) */
    }


    .option-box{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin: 10px auto;
        width: 80%;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
        font-size: 16px;
        font-weight: 500;
        text-align: center;
        transition: all 0.3s ease-in-out;
    }
    .option-box:hover {
        background-color: #f8e1e7;
        transform: translateY(-3px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []

# 질문 리스트 (각 질문별 선택지와 키워드 매핑)
questions = [
    {
      "question": "문득 하늘을 바라보았는데, 갑자기 어떤 감정이 차올랐어. 어떤 감정일까? ☁️",
      "options": {
        "노을을 보고 센티멘털한 감성에 잠겼어": ["sentimental", "melancholy", "nostalgic", "romance", "dramatic", "comforting", "gentle", "whimsical", "awestruck", "admiring", "inspirational", "emotional", "heartfelt", "comingofage"],
        "왠지 희망적이고 행복한 감정이 들었어": ["hopeful", "happy", "uplifting", "cheerful", "excited", "exhilarated", "hilarious", "lighthearted", "amused", "joyous", "enthusiastic"],
        "구름 낀 하늘처럼 갑갑하고 답답한 마음이 들었어": ["gloomy", "tense", "serious", "anxious", "intense", "aggressive", "angry", "cynical", "frantic", "paranoia", "foreboding", "loss of loved one", "trauma", "ptsd", "loneliness", "distressing", "sad"],
        "특별한 감흥 없이 심심하고 무료하게 느껴졌어": ["neutral", "calm", "boring"]
      },
      "note": "그래서… 여행을 떠나기로 했어!"
    },
    {
      "question": "설레는 여행의 시작, 큰 광장에 가보니 사람들이 잔뜩 모여 북적이고 있었는데…",
      "options": {
        "작은 강아지 한 마리가 사람들 사이에서 귀여운 애교를 보여주고 있었어": ["dog", "pets", "animals", "cat", "animal human friendship"],
        "교복을 입은 학생들이 수학여행을 와서 서로 꺄르르 웃으며 대화하고 있었어": ["highschool", "teenmovie", "teenagegirl", "teenageboy", "teenager", "comingofage", "teacher", "school", "bullying", "teencomedy", "teendrama", "romcom", "friendship", "bestfriend", "highschoolstudent", "boardingschool", "prom"],
        "어린 아이들이 밝은 햇살이 비추는 분수에서 즐겁게 놀고 있었어": ["baby", "kids", "child", "parent child relationship", "mother", "father", "mother daughter relationship", "father son relationship", "playful", "orphan", "childprodigy", "parenting"],
        "경찰과 범죄자로 보이는 사람이 서로 대치하고 있었어": ["police", "detective", "cop", "buddycop", "fbi", "cia", "spy", "espionage", "secretagent", "hitman", "assassin", "corruption", "gangster", "organizedcrime", "robbery", "violence", "gun", "shootout", "streetgang", "policechase", "policebrutality", "policecorruption", "undercover", "undercovercop", "conman"]
      },
      "note": ""
    },
    {
      "question": "비를 피하고 있는데, 여행 중 우연히 만난 여행자가 이야기를 시작했어. ☔",
      "options": {
        "숨 막히게 흥미진진한 싸움 경험담": ["fight", "martialarts", "assassin", "hitman", "actionhero", "superhero", "battle", "soldier", "military", "commando", "specialforces", "explosion", "violence", "kaiju", "sword", "swordandsorcery", "femaleassassin", "vigilante", "intense"],
        "납치당할 뻔했던 위험천만한 경험담": ["kidnapping", "hostage", "survival", "suspenseful", "psychologicalthriller", "ontherun", "rescuemission", "prisonescape", "terroristattack", "childkidnapping", "doublecross", "struggleforsurvival"],
        "웃음이 터지는 코믹한 경험담": ["comedy", "standupcomedy", "buddycomedy", "hilarious", "slapstickcomedy", "absurd", "parody", "spoof", "satire", "romcom", "amused", "ridiculous", "actioncomedy"],
        "역사적 유적지에서 겪은 의미 있는 경험담": ["perioddrama", "biography", "basedontruestory", "documentary", "worldwarii", "19thcentury", "1970s", "1940s", "1960s", "victorianengland", "15thcentury", "middleages4761453", "archaeologist", "nazi", "tomb", "historical", "scotland", "basedonmemoirorautobiography"]
      },
      "note": ""
    },
    {
      "question": "여행자가 갑자기 나와 내기를 하고 싶다고 해! 🎲",
      "options": {
        "서로 좋아하는 노래와 댄스 대결로 분위기를 띄워보자!": ["musical", "singer", "dancing", "singing", "concert", "audition", "popmusic", "jukeboxmusical"],
        "몸을 제대로 쓰는 운동 경기로 자웅을 겨뤄보자!": ["sports", "sports documentary", "football", "soccer", "basketball", "martialarts", "boxing", "golf", "competition", "rivalry", "sport competition"],
        "역시 내기에는 게임이지. 게임 내기를 해보자!": ["basedonvideogame", "videogame", "game"],
        "역시 이럴 때는 술내기로 제대로 이겨줘야지!": ["alcoholic", "alcoholism", "drunkenness", "drugdealer", "drugs"]
      },
      "note": ""
    },
    {
      "question": "그런데 갑자기 “꺄악!” 하는 비명 소리가 들리더니… 😱",
      "options": {
        "무기로 무장한 테러리스트와 군인들이 나타나 아수라장이 되었어!": ["terrorism", "military", "soldier", "usnavy", "espionage", "secretagent", "airplane hijacking", "bomb", "explosion", "commando", "specialforces", "nazi", "battle", "worldwarii", "tank"],
        "갑자기 어디선가 좀비들이 나타나 거리 한복판을 헤집고 다니기 시작했어!": ["zombie", "zombieapocalypse", "apocalypse", "postapocalyptic future", "survival", "survivalhorror", "gore", "virus", "struggle for survival", "savingtheworld"],
        "거대한 허리케인이 저 멀리서 빠르게 다가오고 있었어!": ["disaster", "disastermovie", "hurricane", "flood", "tsunami", "storm", "earthquake", "survival", "struggle for urvival"],
        "어? 분명 들렸는데…? 그러나 아무도 없었고, 비명은 환청처럼 사라졌어!": ["ghost", "supernatural", "exorcism", "demon", "psychologicalthriller", "haunting", "hauntedhouse", "possession", "occult", "witch", "wizard", "foundfootage", "devil", "spirit", "cult", "halloween"]
      },
      "note": ""
    },
    {
      "question": "오늘 하루 스쳐간 사건들 속에서, 문득 소중한 누군가가 떠올랐어. 💭",
      "options": {
        "나의 가장 소중한 친구.": ["friendship", "bestfriend", "buddyfilm", "buddycomedy", "friends", "bestfriends", "malefriendship", "groupoffriends", "reunitedfriends"],
        "나를 언제나 믿어주는 가족.": ["family", "familyrelationships", "father daughter relationship", "father sonr elationship", "mother aughter relationship", "mother son elationship", "sibling relationship", "brother brother relationship", "brother sisterr elationship", "parent child relationship", "single mother", "family secrets", "motherhood", "family comedy", "family vacation"],
        "내가 가장 사랑하는 내 연인.": ["love", "romance", "romantic", "fallinginlove", "marriage", "wedding", "extramarital affair", "adultery", "infidelity", "lovetriangle", "loveaffair", "gaytheme", "lgbt", "forbiddenlove", "older woman younger man relationship", "older woman seduces younger guy"],
        "누구보다 소중한 바로 나 자신.": [""]
      },
      "note": ""
    },
    {
      "question": "여행을 떠난 지도 꽤 시간이 흘렀고, 딱 좋아하는 계절이 찾아왔어. 🌸🍂",
      "options": {
        "뜨거운 태양 아래 시원한 바다가 생각나는 여름.": ["summer", "vacation", "holiday", "beach", "roadtrip", "boat"],
        "하얀 눈과 쌀쌀한 날씨의 겨울.": ["winter", "christmas", "snow", "alaska"],
        "따뜻한 기운이 도는 새싹이 반가운 봄.": [""],
        "선선한 바람이 불어오는 낙엽의 가을.": [""]
      },
      "note": ""
    },
    {
      "question": "여행지의 노천 극장에서 상영 중인 영화 한 편이 눈길을 끄네? 🎬",
      "options": {
        "실화를 기반으로 하는 현실감 가득한 다큐멘터리.": ["based on true story", "truecrime", "documentary", "crime documentary", "nature documentary", "biography", "based on ealperson", "based on memoirorautobiography", "historicaldocumentary", "history", "docudrama"],
        "상상력 풍부한 애니메이션, 게임 원작의 작품.": ["anime", "basedonmanga", "basedoncomic", "basedongraphicnovel", "basedonvideogame", "videogame", "cartoon", "3danimation", "animation", "anthropomorphism", "live actionand animation", "adultanimation", "shounen", "kaiju"],
        "잘 알려진 소설 원작의 작품.": ["based on novelor book", "based onc hildrens book", "based on young adult novel", "based on short", "adaptation", "perioddrama", "historicaldrama"],
        "연극이나 뮤지컬 원작의 작품.": ["based on playor musical", "burlesque", "jukeboxmusical", "live action remake"]
      },
      "note": ""
    },
    {
      "question": "여행 마지막날 밤 꿈을 꾸었는데, 흥미로운 꿈을 꾸었어. 🌙",
      "options": {
        "최첨단 세상에서 AI 로봇이 지배하는 미래.": ["artificialintelligenceai", "robot", "dystopia", "postapocalypticfuture", "cyberpunk", "timetravel", "visionofthefuture", "virus", "geneticengineering"],
        "지구와 우주를 오가며 펼쳐지는 박진감 넘치는 우주 활극.": ["space", "spacetravel", "spacecraft", "alien", "alieninvasion", "alienspaceship", "portal", "adventure", "outerspace", "parallelworld"],
        "내가 슈퍼히어로로 변신해서 도시를 구하는 이야기.": ["superhero", "superpower", "superheroteam", "vigilante", "secretidentity", "supervillain", "femalehero", "marvelcinematicuniversemcu", "savingtheworld", "action", "goodversusevil"],
        "전설과 신화 속 용사와 거대한 용이 싸우는 모험.": ["dragon", "fairytale", "wizard", "witch", "king", "princess", "prince", "kingdom", "magic", "swordandsorcery", "supernatural creature", "mythic", "fantasyworld"]
      },
      "note": ""
    },
    {
      "question": "여행을 마치려고 보니, 뭔가 아쉬워. 다음엔 어디를 가보면 좋을까?",
      "options": {
        "아시아 지역 여행.": ["japan", "china", "india", "southkorea", "thailand", "afghanistan", "asia", "tokyo"],
        "미국과 북미 여행.": ["usa", "newyorkcity", "losangeles", "california", "texas", "florida", "illinois", "louisiana", "georgia", "chicago", "newjersey", "neworleans", "atlanta", "seattle", "washington", "michigan"],
        "유럽 여행.": ["england", "france", "italy", "spain", "germany", "sweden", "norway", "scotland", "europe", "london", "paris", "victorianengland", "berlin", "rome"],
        "어디든 좋아! 즐거울 수 있는 곳이라면!": [""]
      },
      "note": "이제 여행을 마치고 집으로 돌아와서, 편안한 마음으로 넷플릭스를 열었더니…!"
    }
]

# 현재 페이지 질문 표시
current_page = st.session_state.page
if current_page <= len(questions):
    q_data = questions[current_page - 1]

    # 질문과 선택지를 하나의 박스 안에 넣기 (HTML + CSS 적용)
    st.markdown(f"""
        <div style="background: #F8E0E6; padding: 25px; border-radius: 15px; color: #4A4A4A;
                    text-align: center; width: 80%; margin: 20px 0 20px 0; 
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); font-size: 14px; 
                    font-weight: bold; display: flex; justify-content: flex-start;">
            <h4>{q_data['question']}</h4>
        </div>
    """, unsafe_allow_html=True)



    # 선택지 박스 (st.radio()를 같은 컨테이너 안에서 표시)
    with st.container():
        options = list(q_data["options"].keys())
        
        selected_option = st.radio("", options, key=f"q{current_page}")

        st.markdown("#### " + q_data["note"])

        st.markdown("</div>", unsafe_allow_html=True)


    # 다음 페이지 버튼
    if st.button("다음", key=f"next{current_page}"):
        st.session_state.answers[f"Q{current_page}"] = selected_option
        # 선택한 키워드를 저장
        selected_keywords = q_data["options"][selected_option]
        st.session_state.selected_keywords.extend(selected_keywords)
        st.session_state.page += 1
        st.rerun()
    
    progress_value = current_page / len(questions)

  
    st.markdown(f"""
        <div style="width: 100%; background-color: #E0E0E0; border-radius: 10px; height: 7px; position: relative; margin-top: 10px;">
            <div style="width: {progress_value * 100}%; background-color: #8A0829; 
                        height: 100%; border-radius: 10px;"></div>
        </div>
        <p style="text-align: center; font-weight: bold; margin-top: 5px;">진행 상태: {current_page}/{len(questions)}</p>
    """, unsafe_allow_html=True)


# 결과 페이지
else:
    df = load_data()

    df["keywords"] = df["keywords"].fillna("")

    # 키워드 매칭 개수 계산 함수
    def count_keyword_matches(row):
        movie_tags = row["keywords"].split(", ")  # 태그를 리스트로 변환
        return sum(tag in st.session_state.selected_keywords for tag in movie_tags)  # 키워드 매칭 개수 카운트

    # 각 영화에 대해 매칭된 키워드 개수를 추가
    df["match_count"] = df.apply(count_keyword_matches, axis=1)

    # 매칭 개수가 많은 순으로 정렬 후 상위 5개 영화만 선택
    df_sorted = df.sort_values(by="match_count", ascending=False).head(5)

    # 결과 출력 (매칭 개수가 1개 이상인 영화만 표시)
    df_filtered = df_sorted[df_sorted["match_count"] > 0]

    # treamlit에서 결과 출력
    st.subheader("🎬 Netflix 추천 컨텐츠 (TOP 5)")
    #st.dataframe(df_sorted[["show_title","category", "weekly_rank", "weekly_views", "keywords", "match_count"]])


    # 영화 상세 정보 및 포스터 가져오기
    for index, row in df_sorted.iterrows():
        movie_title = row["show_title"]
        category = row["category"]
    
        # 카테고리에 따라 API URL 결정
        if category.startswith("Films"):
            search_url = "https://api.themoviedb.org/3/search/movie"
        elif category.startswith("TV"):
            search_url = "https://api.themoviedb.org/3/search/tv"
        else:
            st.write(f"Unknown category for {movie_title}: {category}")
            continue

        # 영화 검색
        params = {
            'api_key': api_key,
            'query': movie_title,
            'language': 'ko'
        }
        response = requests.get(search_url, params=params)
        results = response.json().get('results', [])

        if results:
            movie_id = results[0]['id']
            
            # 영화 상세 정보 가져오기
            details_url = f"https://api.themoviedb.org/3/{'movie' if 'movie' in search_url else 'tv'}/{movie_id}"
            details_params = {
                'api_key': api_key,
                'language': 'ko-KR'
            }
            details_response = requests.get(details_url, params=details_params)
            movie_details = details_response.json()
            print(movie_details)
            
            # 영화 정보 표시 (한 줄 정렬)
            col1, col2 = st.columns([1, 3.5])
            with col1:
                poster_path = movie_details.get('poster_path')
                if poster_path:
                    poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
                    st.image(poster_url, caption=movie_title, use_container_width=True) # container 배포할땐 바꾸기
                else:
                    poster_url = "https://github.com/user-attachments/assets/4b8a1188-7d78-45f9-8cb1-27f94c21c215"
                    st.image(poster_url, caption=movie_title, use_column_width=True)
            
            with col2:
                st.subheader(movie_title)
                st.write(f"**개봉일:** {movie_details.get('release_date', '정보 없음')}")
                st.write(f"**평점:** {movie_details.get('vote_average', '정보 없음')}")
                overview = movie_details.get('overview', '').strip()
                st.write(f"**줄거리:** {overview if overview else '줄거리 정보가 없습니다.'}")

        else:
            st.write(f"{movie_title}: 영화 정보를 찾을 수 없습니다.")

    if st.button("다시 테스트하기"):
        st.session_state.page = 1
        st.session_state.answers = {}
        st.session_state.selected_keywords = []
        st.rerun()


# 🏠 홈으로 가는 버튼 (중앙 정렬)
home_col = st.columns([3, 2, 3])
with home_col[1]:
    if st.button("🏠 Home", key="home"):
        st.switch_page("app.py")  # 홈으로 이동
