import streamlit as st
import requests

# API 정보 설정
API_KEY = "6c7075664f6a756e3130397876735a4a"  # OpenAPI에서 발급받은 인증키 입력
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "citydata"
START_INDEX = 1
END_INDEX = 5
AREA_NAME = "광화문·덕수궁"  # 원하는 지역명을 입력
REQUEST_TYPE = "xml"

# Streamlit UI 구성
st.title("🌤 서울시 실시간 날씨 정보")

# 사용자 입력: 지역 선택
area_options = ["광화문·덕수궁", "강남역", "홍대입구", "서울역", "건대입구"]
selected_area = st.selectbox("날씨를 확인할 지역을 선택하세요:", area_options)

# API 요청 URL 구성
url = f"{BASE_URL}/{API_KEY}/{REQUEST_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{selected_area}"

# API 요청 및 응답
response = requests.get(url)

if response.status_code == 200:
    st.success("✅ 날씨 정보를 성공적으로 가져왔습니다!")
    st.text(response.text)  # XML 데이터를 출력 (향후 JSON 변환 가능)
else:
    st.error(f"❌ 오류 발생: {response.status_code}")

# 실행 방법 안내
st.info("🔹 이 코드는 Streamlit을 통해 실행되며, GitHub에 업로드하여 배포 가능합니다.")
