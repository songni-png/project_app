import requests
import xml.etree.ElementTree as ET

# API 정보 설정
API_KEY = "6c7075664f6a756e3130397876735a4a"  # OpenAPI에서 발급받은 인증키 입력
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "citydata"
START_INDEX = 1
END_INDEX = 5
REQUEST_TYPE = "xml"

def get_weather_info(area_name):
    """
    서울시 실시간 도시데이터 API를 호출하여 특정 지역의 날씨 정보를 가져오는 함수
    :param area_name: 요청할 지역명 (예: '광화문·덕수궁')
    :return: 날씨 정보 (없을 경우 '날씨 정보 없음')
    """
    url = f"{BASE_URL}/{API_KEY}/{REQUEST_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{area_name}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)

        # AREA_NM 및 WEATHER_STTS 추출
        area_nm = root.find(".//AREA_NM").text if root.find(".//AREA_NM") is not None else "정보 없음"
        weather_stts = root.find(".//WEATHER_STTS").text if root.find(".//WEATHER_STTS") is not None else "날씨 정보 없음"

        return {"location": area_nm, "weather": weather_stts}
    else:
        return {"error": f"❌ 서버 오류 발생: {response.status_code}"}

# 테스트 실행
if __name__ == "__main__":
    test_location = "광화문·덕수궁"
    weather_data = get_weather_info(test_location)
    print(weather_data)
