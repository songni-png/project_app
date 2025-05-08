import requests
import xml.etree.ElementTree as ET
import csv
import os

API_KEY = "6c7075664f6a756e3130397876735a4a"
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "citydata"
START_INDEX = 1
END_INDEX = 5
REQUEST_TYPE = "xml"
CSV_FILE = os.path.join(os.getcwd(), "locations_utf8.csv")


def load_locations(file_path):
    locations = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            locations[row["AREA_NM"]] = row["AREA_CD"]
    return locations

locations = load_locations(CSV_FILE)

def get_weather_info(area_name):
    area_code = locations.get(area_name)
    if not area_code:
        return {"error": "지역명이 올바르지 않습니다."}

    url = f"{BASE_URL}/{API_KEY}/{REQUEST_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{area_code}"
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        weather_element = root.find(".//WEATHER_STTS")
        temp_element = root.find(".//TEMP")
        sensible_temp_element = root.find(".//SENSIBLE_TEMP")
        humidity_element = root.find(".//HUMIDITY")
        wind_element = root.find(".//WIND_SPD")
        precpt_element = root.find(".//PRECPT_TYPE")

        weather_stts = weather_element.text if weather_element is not None else "정보 없음"
        temp = temp_element.text if temp_element is not None else "정보 없음"
        sensible_temp = sensible_temp_element.text if sensible_temp_element is not None else "정보 없음"
        humidity = humidity_element.text if humidity_element is not None else "정보 없음"
        wind_speed = wind_element.text if wind_element is not None else "정보 없음"
        precipitation = precpt_element.text if precpt_element is not None else "정보 없음"

        return {
            "지역명": area_name,
            "날씨": weather_stts,
            "기온": temp,
            "체감온도": sensible_temp,
            "습도": humidity,
            "풍속": wind_speed,
            "강수 유형": precipitation
        }
    else:
        return {"error": f"서버 오류: {response.status_code}"}
