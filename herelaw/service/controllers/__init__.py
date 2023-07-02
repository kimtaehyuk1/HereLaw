from flask import (
    render_template,
    request,
    jsonify,
    make_response,
    url_for,
    session,
    redirect,
)
import jwt
from service.config import *
from service.models import chat_gpt, search, weather, image
from service import app
import uuid
import json
from datetime import datetime
import pytz
from service import db
import os
import time
import re

app.secret_key = APP_SECRET_KEY


# 시작화면 - 시작시 위치를 확인 할 수 있는 템플릿 전송
@app.route("/")
def home():
    # JWT 데이터 정의
    user_unique = uuid.uuid4().hex

    # JWT 생성
    token = {"user_unique": user_unique, "chat_cnt": 0}
    token = jwt.encode(token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    # 유니크한 세션 생성
    session["user_unique"] = user_unique

    # 쿠키에 JWT 저장
    # response = make_response(render_template("chatbot_test.html"))
    response = make_response(render_template("guide.html"))
    response.set_cookie("token", token)

    return response


@app.route("/result", methods=["GET", "POST"])
def result():
    return render_template("result.html")


# 룰 기반 채팅
@app.route("/role_chat", methods=["GET", "POST"])
def role_chat():
    # 사용자의 입력
    user_input = request.get_json()
    print(user_input)

    # 사용자의 입력 받아오기
    answer = []
    for item in user_input["conversation"]:
        answer.append(item["answer"])

    # 사용자의 입력 쿼리화
    # 첫번째 카테고리는 세션으로 받기
    what = session.get("what")

    query = f"{what}사고가 났고,{answer[0]}에서 사고가 났으며, 나는 {answer[1]} 진행하였고, 상대방은{answer[2]} 진행하였다."
    form_result = chat_gpt.chatgpt_form(query)
    print(form_result)
    pattern = r"{([\s\S]*?)}"
    form_result = re.search(pattern, form_result)[0]
    form_result = form_result.replace('"', "'")

    print("----------------------------")
    print(form_result)

    # 위치와 날씨 정보 받아오기
    latitude = session.get("latitude")
    longitude = session.get("longitude")
    weather_result = weather.find_location(latitude, longitude)

    final_position = weather_result["location"]
    final_weather = weather_result["weather"]["precipitation_form"]

    name = session["file_path"]

    # 현재 날짜 받기
    korea_timezone = pytz.timezone("Asia/Seoul")
    current_date = datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")

    # 협의서 그리기
    image.report_input(
        query, final_position, final_weather, current_date, name, latitude, longitude
    )

    # 쿼리를 이용해 유사한 비율, 판례 검색
    rate = search.rate_search(form_result)
    law = search.law_search(form_result)


    # 제보문 작성하기
    report = chat_gpt.lawyer_report(query)

    # 필요한 모든 정보 반환
    res = {
        "ratio": rate["rate"],  # 과실비율
        "ratio_com": rate["rate_com"],  # 과실비율 해설 요약
        "res_gpt": law['res'],  # 판례 요약
        "guide": "None",  # 대응 가이드
        "ins_info": "None",  # 보험사 정보
        "message": "herelaw가 분석중입니다.",
        "agreement": "pic",
        "lawyer_text": report,
    }
    # print(res)

    # 필요 정보들 세션값으로 저장
    if "user_unique" in session:
        # 과실비율
        session["rate"] = res["ratio"]
        # 과실비율 요약
        session["rate_com"] = res["ratio_com"]
        # 판례 요약
        session["law"] = res["res_gpt"]
        # 변호사 제보문
        session["report"] = res["lawyer_text"]

        # 데이터 베이스에 로그값들 저장
        # db.insert_log(
        #     user_id = str(session["user_unique"]),           # 유니크한 유저id
        #     query = query,                                   # 사용자 입력 쿼리(대화)
        #     rate = rate["rate"],                             # 과실비율
        #     rate_name = rate["name"] ,                       # 찾은 과실파일 이름
        #     law_name = law["name"]                           # 찾은 판례파일 이름
        # )

    return jsonify(res)


@app.route("/chat_chat", methods=["GET", "POST"])
def chat_chat():
    # 내가 사용할 데이터
    my_msg = BASIC_GPT_MSG.copy()

    # 사용자의 입력 받기
    req = request.get_json()["message"]

    # 사용자의 기본 토큰 받기
    token = request.cookies.get("token")
    token = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHMS)

    # 사용자의 대화 횟수 정의
    chat_cnt = int(token.get("chat_cnt"))

    # 사용자의 대화 내역 토큰들 받기
    answer_tokens = []
    for i in range(chat_cnt):
        answer_tokens.append(
            jwt.decode(
                request.cookies.get(f"answer_token_{i}"),
                JWT_SECRET_KEY,
                algorithms=JWT_ALGORITHMS,
            )
        )

    # 대화가 종료 되었을때
    if chat_cnt == 2:
        for answer_token in answer_tokens:
            my_msg.append(answer_token["user"])
            my_msg.append(answer_token["bot"])

        # 대화내용을 db에 넣기 위해
        chat_db = str(my_msg)
        chat_db = chat_db.replace("'", "/'").replace('"', "/'")

        # 폼GPT로 우리데이터 형태로 변환
        final_res = my_msg[-1]["content"]
        print(final_res)
        form_result = chat_gpt.chatgpt_form(final_res)
        pattern = r"{([\s\S]*?)}"
        form_result = re.search(pattern, form_result)[0]
        form_result = form_result.replace('"', "'")

        print("----------------------------")
        print(form_result)

        # 위치와 날씨 정보 받아오기
        latitude = session.get("latitude")
        longitude = session.get("longitude")
        precipitation_form = session.get("precipitation_form")
        location = session.get("location")

        final_position = location
        final_weather = precipitation_form

        # 현재 날짜 받기
        korea_timezone = pytz.timezone("Asia/Seoul")
        current_date = datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")

        name = session.get("file_path")

        # 협의서 그리기
        image.report_input(
            form_result, final_position, final_weather, current_date, name
        )  # (특이사항칸에 쓰는거, 최종 위치, 최종 날씨)

        # GPT통해 나온 최종 폼을 바탕으로 검색시작
        rate = search.rate_search(form_result)
        law = search.law_search(form_result)


        # 제보문 작성하기
        report = chat_gpt.lawyer_report(form_result)
        print("----------------------------")
        print(report)

        res = {
            "rate": rate["rate"],  # 과실비율
            "rate_com": rate["rate_com"],  # 과실비율 해설 요약
            "law": law["res"],  # 판례 요약
            "guide": None,  # 대응 가이드
            "ins_info": None,  # 보험사 정보
            "message": "done",
            "count": chat_cnt,
            "lawyer_text": report,
        }

        # 필요 정보들 세션값으로 저장
        if "user_unique" in session:
            # 과실비율
            session["rate"] = res["rate"]
            # 과실비율 요약
            session["rate_com"] = res["rate_com"]
            # 판례 요약
            session["law"] = res["law"]
            # 변호사 제보문
            session["report"] = res["lawyer_text"]

            # 데이터 베이스에 로그값들 저장
            # db.insert_log(
            #     user_id = str(session["user_unique"]),           # 유니크한 유저id
            #     query = chat_db,                                   # 사용자 입력 쿼리(대화)
            #     rate = rate["rate"],                             # 과실비율
            #     rate_name = rate["name"],                       # 찾은 과실파일 이름
            #     law_name = law["name"]                           # 찾은 판례파일 이름
            # )

        # 결과 반환
        return jsonify(res)
        # return redirect(url_for('result', fi_data=json.dumps(res)))

    # 대화 중일때
    else:
        token["chat_cnt"] += 1

        print(token["chat_cnt"])

        # 기존 대화 붙여넣기
        for answer_token in answer_tokens:
            my_msg.append(answer_token["user"])
            my_msg.append(answer_token["bot"])

        # print(my_msg)

        usr, bot, res_gpt = chat_gpt.chatgpt_res(my_msg, req)

    # 사용자에게 줄 토큰 생성
    return_answer_token = {
        "user_unique": token["user_unique"],
        "user": usr,
        "bot": bot,
    }

    # 사용자에게 줄 기본 토큰
    token = jwt.encode(token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    # 사용자에게 줄 엔서 토큰
    return_answer_token = jwt.encode(
        return_answer_token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )

    # 데이터 전송 및, 쿠키에 JWT 저장
    response = make_response(jsonify({"message": res_gpt, "count": chat_cnt}))
    response.set_cookie("token", token)
    response.set_cookie(f"answer_token_{chat_cnt}", return_answer_token)

    return response


@app.route("/ratiooverlay", methods=["GET"])
def ratiooverlay():
    rate = session.get("rate")
    rate_com = session.get("rate_com")
    print(rate)
    print(rate_com)
    return jsonify({"rate": rate, "rate_com": rate_com})


@app.route("/lawoverlay", methods=["GET"])
def lawoverlay():
    law = session.get("law")
    return jsonify({"law": law})


@app.route("/laweroverlay", methods=["GET"])
def laweroverlay():
    report = session.get("report")
    return jsonify({"report": report})


@app.route("/client_keyword", methods=["POST"])
def client_keyword():
    # data = {
    #   road: 길 이름 (고속도로, 차대차, ...)
    #   latitude: 위도
    #   longitude: 경도
    # }

    file = request.files["file"]
    data = json.loads(request.form.get("data"))

    print(file, data)

    # 위치를 이용해 날씨 API 사용
    weather_result = weather.find_location(data["latitude"], data["longitude"])

    # request.form.get()
    if "user_unique" in session:
        filename = str(session["user_unique"]) + "+" + str(time.time()) + ".jpg"
        file.save(os.path.join("herelaw/service/uploads/pictures", filename))

        session["what"] = data["road"]
        session["latitude"] = data["latitude"]
        session["longitude"] = data["longitude"]
        session["file_path"] = filename
        session["location"] = weather_result["location"]
        session["temperature"] = weather_result["weather"]["temperature"]
        session["precipitation_form"] = weather_result["weather"]["precipitation_form"]
        session["precipitation"] = weather_result["weather"]["precipitation"]
    return ""


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    # print(session)
    return render_template("chatbot_test.html")


@app.route("/get_file_name", methods=["GET", "POST"])
def get_file_name():
    session.get("file_path")
    return session.get("file_path")
