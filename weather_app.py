import requests
import xml.etree.ElementTree as ET
import csv
import os

# API 정보 설정
API_KEY = "6c7075664f6a756e3130397876735a4a"
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "citydata"
START_INDEX = 1
END_INDEX = 5
REQUEST_TYPE = "xml"
# CSV 파일 경로 설정 (현재 디렉토리에서 찾기)
CSV_FILE = os.path.join(os.getcwd(), "locations.csv")
print(CSV_FILE)


def load_locations(file_path):
    """
    CSV 파일을 읽어 AREA_CD와 AREA_NM 데이터를 딕셔너리로 저장
    """
    locations = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            locations[row["AREA_CD"]] = row["AREA_NM"]
    return locations

# CSV 파일에서 데이터 로드
locations = load_locations(CSV_FILE)

def get_weather_info(area_code):
    """
    서울시 실시간 도시데이터 API를 호출하여 특정 지역의 날씨 정보를 가져오는 함수
    :param area_code: 요청할 지역 코드 (예: 'POI009')
    :return: 날씨 정보 (없을 경우 '날씨 정보 없음')
    """
    url = f"{BASE_URL}/{API_KEY}/{REQUEST_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{area_code}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)

        # AREA_NM 및 WEATHER_STTS 추출
        area_nm = locations.get(area_code, "정보 없음")  # CSV에서 지역명 매핑
        weather_element = root.find(".//WEATHER_STTS")

        weather_stts = weather_element.text if weather_element is not None and weather_element.text else "날씨 정보 없음"

        return {"location": area_nm, "weather": weather_stts}
    else:
        return {"error": f"❌ 서버 오류 발생: {response.status_code}"}

# 테스트 실행
if __name__ == "__main__":
    test_code = "POI009"  # 광화문·덕수궁의 AREA_CD
    weather_data = get_weather_info(test_code)
    print(weather_data)
