import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval
import json
from geopy.distance import geodesic
import os

os.system("pip install streamlit-js-eval==0.1.7")


st.set_page_config(page_title="회복 루틴 추천기", page_icon="🧘", layout="centered")

# 1. 위치 정보 가져오기 (비동기 Promise 방식)
loc = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (pos) => resolve({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
            (err) => reject(err)
        );
    })
    """,
    key="get_location_with_coords"
)

# 2. 사용자 UI
st.title("🧘 회복이 필요한 날을 위한 맞춤 루틴 추천기")

now = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(f"⏰ 현재 시간: {now}")

activity = st.radio("오늘 얼마나 활동하셨나요?", ["많이 움직였어요", "적당히 움직였어요", "거의 안 움직였어요"])
social = st.radio("얼마나 사람을 만나셨나요?", ["많은 사람을 만났어요", "혼자 있었어요"])
tag = st.selectbox("원하는 회복 태그를 골라주세요", ["힐링", "에너지","감정 정화","감정 자극", "집중력", "안정"])

# 3. 위치 정보 출력
if loc and isinstance(loc, dict) and "latitude" in loc:
    lat, lon = loc["latitude"], loc["longitude"]
    st.success(f"📍 현재 위치: 위도 {lat:.5f}, 경도 {lon:.5f}")
else:
    st.info("📡 위치 정보를 불러오는 중이거나, 위치 권한이 허용되지 않았습니다.")
    lat, lon = None, None

# 데이터 파일 경로 설정
DATA_FILE = r"C:\Users\soyoe\OneDrive\바탕 화면\홍익대학교\4학년\1학기\시스템분석\Project Data\tag_coordi_.csv"
WEATHER_DATA_FILE = r"C:\Users\soyoe\OneDrive\바탕 화면\홍익대학교\4학년\1학기\시스템분석\Project Data\장소별_날씨_결과.csv"

# 데이터 로드 함수
def load_data():
    return pd.read_csv(DATA_FILE, encoding="cp949")

def load_weather_data():
    return pd.read_csv(WEATHER_DATA_FILE, encoding="cp949")

# 데이터 로드 및 병합 (초기 1회)
place_df = load_data()
weather_df = load_weather_data()
place_df = place_df.merge(weather_df, on=["NAME", "LAT", "LON"], how="left")


# 거리 계산 및 반경 2km 필터
radius = st.slider("추천 반경 (km)", 1.0, 5.0, 2.5, step=0.1)
st.session_state.radius_value = radius

# 4. 루틴 추천 실행
if st.button("회복 루틴 추천받기"):
    with st.spinner("당신에게 맞는 장소를 찾는 중입니다..."):
        df = place_df.copy()
        
        # 필수 열이 있는지 체크 및 결측 제거
        df = df.dropna(subset=["LAT", "LON"])
        df["LAT"] = df["LAT"].astype(float)
        df["LON"] = df["LON"].astype(float)

        # 태그 필터링
        df = df[df["TAG"].notna() & df["TAG"].str.contains(tag)].head(5)

        # 거리 계산 함수 정의
        def compute_distance(row):
            try:
                return geodesic((lat, lon), (row["LAT"], row["LON"])).km
            except:
                return None

        if lat and lon:
            df["DIST_KM"] = df.apply(compute_distance, axis=1)
            df = df.dropna(subset=["DIST_KM"])
            nearby_df = df[df["DIST_KM"] <= radius].sort_values(by="DIST_KM")
        else:
            nearby_df = df

        # 추천 결과 출력
        st.markdown(f"## 📌 반경 {st.session_state.radius_value}km 이내 추천 장소")
        if nearby_df.empty:
            st.warning(f"조건에 맞는 장소가 반경 {st.session_state.radius_value}km 이내에 없습니다 😢")
        else:
            for _, row in nearby_df.iterrows():
                st.markdown(f"### 🏞️ {row['NAME']}")
                st.markdown(f"- 📍 위치: {row['LOCATION']}")
                st.markdown(f"- 🏷️ 태그: {row['TAG']}")
                st.markdown(f"- 📏 거리: 약 {row['DIST_KM']:.2f} km")
                st.markdown("---")

                # 장소별 날씨 정보 추가
                st.markdown(f"🌤️ **{row['NAME']} 근처 날씨 정보**")
                st.write(f"- 날씨 상태: {row.get('weather', '정보 없음')}")
                st.write(f"- 기온: {row.get('temperature', '정보 없음')}°C")
                st.write(f"- 습도: {row.get('humidity', '정보 없음')}%")
                
                st.markdown("---")
                
        

            # 지도 시각화
            st.markdown("### 🗺️ 지도에서 추천 장소 보기")
            map_df = nearby_df[["LAT", "LON"]].rename(columns={"LAT": "lat", "LON": "lon"})
            st.map(map_df, use_container_width=True)

