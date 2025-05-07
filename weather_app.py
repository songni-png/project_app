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
    url = f"{BASE_URL}/{API_KEY}/{REQUEST_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{area_name}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)

        area_nm_element = root.find(".//AREA_NM")
        weather_element = root.find(".//WEATHER_STTS")
        temp_element = root.find(".//TEMP")  # 온도 데이터 확인
        humidity_element = root.find(".//HUMIDITY")  # 습도 데이터 확인

        area_nm = area_nm_element.text if area_nm_element is not None else "정보 없음"
        weather_stts = weather_element.text if weather_element is not None and weather_element.text else "날씨 정보 없음"
        temp = temp_element.text if temp_element is not None else "온도 정보 없음"
        humidity = humidity_element.text if humidity_element is not None else "습도 정보 없음"

        return {
            "location": area_nm,
            "weather": weather_stts,
            "temperature": temp,
            "humidity": humidity
        }
    else:
        return {"error": f"❌ 서버 오류 발생: {response.status_code}"}

# 테스트 실행
if __name__ == "__main__":
    test_location = "광화문·덕수궁"
    weather_data = get_weather_info(test_location)
    print(weather_data)
