import streamlit as st
import requests
import xml.etree.ElementTree as ET

# API 정보 설정
API_KEY = "6c7075664f6a756e3130397876735a4a"  # OpenAPI에서 발급받은 인증키 입력
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "citydata"
START_INDEX = 1
END_INDEX = 5
REQUEST_TYPE = "xml"

# 날씨 정보를 가져오는 함수
def get_weather_info(area_name):
    url = f"{BASE_URL}/{API_KEY}/{REQUEST_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{area_name}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        weather_data = root.find(".//WEATHER_STTS").text if root.find(".//WEATHER_STTS") is not None else "정보 없음"
        return weather_data
    else:
        return f"❌ 오류 발생: {response.status_code}"
    st.error(f"❌ 오류 발생: {response.status_code}")

# 실행 방법 안내
st.info("🔹 이 코드는 Streamlit을 통해 실행되며, GitHub에 업로드하여 배포 가능합니다.")
