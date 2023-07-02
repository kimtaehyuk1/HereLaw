import pandas as pd
import requests
from haversine import haversine
from service.config import *
from datetime import datetime, timedelta
from pytz import timezone
import json


# 기상청 API에서 사용하는 위치와 위도 경도를 매칭하는 테이블 불러오기
def raed_location_table():
    df = pd.read_csv("herelaw/service/data/location_data.csv", index_col=0)
    return df


# 데이터 테이블 세팅
DATA_TABLE = raed_location_table()


# 현재 날씨를 받아오는 함수
def get_now_weather(x, y):
    # 현재 시간 측정
    now_time = datetime.now() - timedelta(minutes=41)

    base_date = f"{now_time.year:0>4}" + f"{now_time.month:0>2}" + f"{now_time.day:0>2}"
    base_time = f"{now_time.hour:0>2}" + "00"

    params = {
        "serviceKey": WEATHER_API_KEY,
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": x,
        "ny": y,
    }

    # 기상청 API에 요청
    response = requests.get(WEATHER_API_URL, params=params)

    # 날씨와 매칭되는 각각의 내용
    wanted_data = {
        "T1H": "temperature",
        "RN1": "precipitation",
        "PTY": "precipitation_form",
        "WSD": "wind_speed",
    }
    # 날씨 세분화를 위한 각각의 내용
    precipitation_form = {
        "0": "맑음",
        "1": "비",
        "2": "비/눈",
        "3": "눈",
        "5": "빗방울",
        "6": "빗방울, 눈날림",
        "7": "눈날림",
    }

    weather = {}

    # 전송받은 결과에서 필요한 데이터 추출 (기온(temperature), 강수형태(precipitation_form), 강수량(precipitation),  풍속(wind_speed))
    for res in json.loads(response.content)["response"]["body"]["items"]["item"]:
        if res["category"] in wanted_data:
            # 각각의 데이터의 이름을 적당한 이름으로 변환
            # 강수 형태일 경우 추가 설명
            weather[wanted_data[res["category"]]] = (
                res["obsrValue"]
                if wanted_data[res["category"]] != "precipitation_form"
                else precipitation_form[res["obsrValue"]]
            )

    return weather


# 사용자의 위경도를 입력받아 위치와 날씨를 반환하는 메소드
def find_location(latitude, longitude):
    """_summary_

    Args:
        latitude (float): 위도
        longitude (float): 경도

    Returns:{
            "location": 위치 (ex. 서울특별시 중구 장충동),
            "weather": {
                "temperature": 온도 [℃],
                "precipitation": 한시간 강수량 [범주 (1 mm)],
                "precipitation_form": 강수형태 (ex. 특이사항 없음, 눈, 비, 눈/비),
                "wind_speed": 풍속 [m/s],
                }
        }
    """

    # 사용자의 위도 경도
    user_location = (latitude, longitude)

    min = -1
    num = -1

    # 테이블에서 사용자의 위치와 가장 가까운 장소 데이터 반환
    for i in range(len(DATA_TABLE)):
        # 세부 시/군/구/동이 없는 데이터 배제
        if len(DATA_TABLE.iloc[i]["location"].split(" ")) < 3:
            continue

        data_loaction = (
            DATA_TABLE.iloc[i]["latitude"],
            DATA_TABLE.iloc[i]["longitude"],
        )
        dist = haversine(user_location, data_loaction, unit="m")

        # 최소 거리 비교
        if min != -1:
            if dist < min:
                min = dist
                num = i
        else:
            min = dist
            num = i

    weather = get_now_weather(DATA_TABLE.iloc[num]["x"], DATA_TABLE.iloc[num]["y"])

    return {
        "location": DATA_TABLE.iloc[num]["location"],
        "weather": weather,
    }  # 위치


if __name__ == "__main__":
    print(find_location(36.363042491373854, 127.37209406168083))
