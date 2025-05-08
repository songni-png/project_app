import streamlit as st
import pandas as pd
import os
from weather_app import get_weather_info, locations

# 데이터 경로 설정
data_path = os.path.abspath('activity.xlsx')

# 감정 ↔ 회복 방향 ↔ 추천 콘텐츠 매핑
mapping_data = {
    "행복": ["예술 전시", "음악 공연", "크리에이티브 클래스"],
    "활력있는": ["스포츠 활동", "카페 탐방", "파티/소셜 모임"],
    "공허함": ["독서", "힐링 산책로", "명상 클래스"],
    "번아웃": ["힐링 카페", "스파/온천", "고요한 공간"],
    "스트레스": ["액티비티 체험 (방탈출, 클라이밍)", "요가"],
    "무기력": ["춤", "피트니스", "음악 듣기", "야외 활동"],
    "조급함": ["조용한 독서 공간", "플랜 짜기", "서점 방문"],
    "슬픔": ["감성 전시회", "조용한 카페", "힐링 음악"],
    "불안": ["자연 속 산책", "명상", "따뜻한 음식점"],
    "짜증": ["격렬한 스포츠 활동", "게임 카페", "드라이브"],
    "혼란": ["퍼즐/보드게임", "독서", "생각 정리 공간"],
    "우울": ["공동 취미 모임", "친환경 카페", "대화 공간"]
}

# 장소 데이터 로드
DATA_FILE = "장소별 감정 TAG_with_coords.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE, encoding="utf-8-sig")

df = load_data()

# -----------------------
# 1. 위치 정보 가져오기
# -----------------------
loc = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (pos) => resolve({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
            (err) => reject(err)
        );
    })
    """,
    key="get_location_promise"
)

# Streamlit UI 구성
st.title("🎭 감정 기반 루틴 추천 시스템")

now = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(f"⏰ 현재 시간: {now}")

activity = st.radio("오늘 얼마나 활동하셨나요?", ["많이 움직였어요", "적당히 움직였어요", "거의 안 움직였어요"])
social = st.radio("얼마나 사람을 만나셨나요?", ["많은 사람을 만났어요", "혼자 있었어요"])
tag = st.selectbox("원하는 회복 태그를 골라주세요", ["힐링", "에너지", "감정 정화", "집중력", "안정"])

# -----------------------
# 3. 위치 상태 확인
# -----------------------
if loc and isinstance(loc, dict) and "latitude" in loc:
    lat, lon = loc['latitude'], loc['longitude']
    st.success(f"📍 현재 위치: 위도 {lat:.5f}, 경도 {lon:.5f}")
else:
    st.warning("📡 위치 정보를 불러오지 못했습니다. 위치 권한을 확인하세요.")
    
# 사용자 입력
emotion = st.selectbox("현재 기분을 선택하세요", list(mapping_data.keys()))
recovery_direction = st.selectbox("회복 방향을 선택하세요", ["위로", "감정 정화", "에너지 회복", "집중력 회복", "안정", "감정 자극", "사회적 연결", "몰입", "스트레스 해소", "소통"])
weather = st.selectbox("현재 날씨를 선택하세요", ["맑음", "흐림", "비", "눈", "강풍"])
time_of_day = st.selectbox("현재 시간대를 선택하세요", ["아침", "점심", "저녁"])
area_name = st.selectbox("지역을 선택하세요:", list(locations.keys()), key="area_name_select")
radius = st.slider("추천 반경 (km)", 10, 30, 20)

if st.button("회복 루틴 추천받기"):
    with st.spinner("당신에게 맞는 루틴을 구성 중입니다..."):
        def match_tags(tags_str):
            if pd.isna(tags_str):
                return False
            return tag in tags_str

        filtered = df[df["TAG"].apply(match_tags)]

        st.markdown("## 📌 추천 루틴")
        for _, row in filtered.iterrows():
            st.markdown(f"### 🏞️ {row['NAME']}")
            st.markdown(f"- 📍 위치: {row['LOCATION']}")
            st.markdown(f"- 🧾 유형: {row['TYPE']}")
            st.markdown(f"- 🔖 태그: {row['TAG']}")
            st.markdown("—")

# weather_app.py에서 날씨 데이터 가져오기
weather_info = get_weather_info(area_name)

# 버튼 클릭 시 API 호출
if st.button("날씨 조회하기"):
    result = get_weather_info(area_name)
    
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader(f"{result['지역명']} 날씨 정보")
        st.write(f"**날씨**: {result['날씨']}")
        st.write(f"**기온**: {result['기온']}℃")

    st.subheader("📚 도서관 추천")
    filtered_libs = lib_data[lib_data["address2"] == location].head(5)
    st.write(filtered_libs[["lib_name", "addr"]])

    st.subheader("🚶‍♂️ 산책로 추천")
    filtered_walks = walk_data[walk_data["address2"] == location].head(3)
    st.write(filtered_walks[["walk_name", "addr"]])

    st.subheader("🎨 추천 활동")
    filtered_activities = activity_data[activity_data["address2"] == location].head(3)
    st.write(filtered_activities[["activity_name", "addr"]])

    st.success("🎯 해당 조건에 맞는 장소와 활동을 검색하여 추천할 수 있습니다!")
