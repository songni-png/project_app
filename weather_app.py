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
CSV_FILE = "C://Users//soyoe//OneDrive//바탕 화면//홍익대학교//4학년//1학기//시스템분석//Project Data//locations.CSV"

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

    print(response.text) 
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        hotspot = root.find(".//row")
        if hotspot is None:
            return {"error": "해당 지역에 데이터가 없습니다."}

        weather_stts_node = hotspot.find("WEATHER_STTS")
        if weather_stts_node is not None:
            temp = weather_stts_node.findtext("TEMP", "정보 없음")
            weather_time = weather_stts_node.findtext("WEATHER_TIME", "정보 없음")
        else:
            temp = "정보 없음"
            weather_time = "정보 없음"

        address = hotspot.findtext("STAT_ADDR", "정보 없음")
        lat = hotspot.findtext("LAT", "정보 없음")
        lng = hotspot.findtext("LNG", "정보 없음")

        return {
            "지역명": area_name,
            "관측시간": weather_time,
            "기온": temp,
            "주소": address,
            "위도": lat,
            "경도": lng
        }
    else:
        return {"error": f"서버 오류: {response.status_code}"}

