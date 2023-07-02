import requests
import re
from service.config import *
from service.models import chat_gpt, fault_rate_match
from flask import request 


# 과실비율 파싱
def rate_search_parser(data, data_name):
    # 과실비율
    rate_pattern = r"\[\[과실비율\]\]([\s\S]*?)\[\[카테고리 및 분류\]\]"
    rate = re.findall(rate_pattern, data)[0]

    # 과실비율 해설
    rate_com = fault_rate_match.match(data_name)

    # 과실비율 해설 요약
    rate_com = chat_gpt.short_summary(rate_com)

    return {"rate": rate, "rate_com": rate_com}


# 판례, 분쟁심의 파싱
def law_search_parser(name, data):
    # 판례일 경우
    if "law_case" in name:
        # 판례 절반 나누기
        flag = len(data) // 2
        data1 = data[:flag]
        data2 = data[flag:]

        # 판례 중 1개를 미리 요약 후 합쳐서 요약 (토큰 수 제한으로 인해)
        data1 = chat_gpt.short_summary(data1)
        res = chat_gpt.long_summary(data1, data2)

        return res

    # 분쟁심의일 경우
    elif "dispute_review" in name:
        # 내용 파싱
        pattern = r"사고 내용:([\s\S]*?)결정 이유:"
        res = re.findall(pattern, data)[0]

        # # 분쟁심의 절반 나누기
        # flag = len(data) // 2
        # data1 = data[:flag]
        # data2 = data[flag:]

        # # 분쟁심의 중 1개를 미리 요약 후 합쳐서 요약 (토큰 수 제한으로 인해)
        # data1 = chat_gpt.short_summary(data1)
        res = chat_gpt.short_summary(data)

        return res

    else:
        return ""


# 과실비율 검색
def rate_search(query):
    """
    return: {"rate": rate, "rate_com": rate_com, "name": file_name}
    """

    # API 서버
    url = f"{API_SERVER_URL}/rate/bm"

    # API 서버에 맞게 데이터 정의
    data = {"query": query, "k": 1}

    # API 서버에 데이터 요청
    res = requests.post(url, json=data).json()

    # 결과 파싱
    rate = rate_search_parser(res[0]["content"], res[0]["meta"]["name"])

    return {"rate": rate["rate"], "rate_com": rate["rate_com"], "name": res[0]["meta"]["name"]}


# 판례 & 분쟁심의 검색
def law_search(query):
    """
    return: { res: 요약된 내용, name: file_name }
    """
    # API 서버
    url = f"{API_SERVER_URL}/law/bm"

    # API 서버에 맞게 데이터 정의
    data = {"query": query, "k": 1}

    # API 서버에 데이터 요청
    res = requests.post(url, json=data).json()
    name = res[0]["meta"]["name"]

    # 결과 파싱
    res = law_search_parser(name=res[0]["meta"]["name"], data=res[0]["content"])

    return {"res": res, "name": name}
