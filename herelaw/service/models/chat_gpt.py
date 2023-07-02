from service.config import *
import openai
import pandas as pd

openai.api_key = OPEN_AI_API_KEY



# (짧은) 입력받은 데이터를 요약
def short_summary(data):
    completion = openai.ChatCompletion.create(
        model=CHAT_GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "당신은 어려운 법 문서를 어린아이도 쉽게 읽을 수 있게 요약해주는 요약가 입니다.",
            },
            {
                "role": "user",
                "content": f"당신이 쉽게 요약할 문서는 <{data}> 이것이고, 3줄로 요약해줘.",
            },
        ],
        temperature=0.5,
    )
    # 결과 응답
    res = completion["choices"][0].message.content
    return res


# (긴) 입력받은 데이터를 요약
def long_summary(data1, data2):
    completion = openai.ChatCompletion.create(
        model=CHAT_GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "당신은 어려운 법 문서를 어린아이도 쉽게 읽을 수 있게 요약해주는 요약가 입니다.",
            },
            {
                "role": "user",
                "content": f"당신은 <{data1}> 과 <{data2}> 조합하여 3줄로 요약해.",
            },
        ],
        temperature=0.5,
    )
    # 결과 응답
    res = completion["choices"][0].message.content
    return res


def chatgpt_form(data):

    #data_path = 'service/data/rate_full.xlsx'
    #excel  = pd.read_excel( data_path )

    completion = openai.ChatCompletion.create(
            model=CHAT_GPT_MODEL,
            messages=[
        {"role": "system", "content": "당신은 응답이 들어오면, 응답내용 중 조합한 정보를 json형태로 바꿔주어야 하는 임무가 있습니다."},
        {"role": "system", 
        "content": """당신이 바꿔야할 json 형식은
                    {
                            "사고종류": "<채워야 할 내용>",
                            "사고원인": "<채워야 할 내용>",
                    }
        이고, 사고원인에는 장소가 포함되어 있어야 합니다!"""},
        {"role": "user", "content": f"응답은  {data} 입니다.'"},
        {"role": "user", "content": f" 중요: 응답내용중 조합한 정보를 바탕으로 json형식에서 <채워야 할 내용>만 채워서 알려주세요. 사고종류와 사고원인만 있으면 됩니다! "},
            ],
        temperature=0
        )
    
    res_gpt = completion["choices"][-1].message.content #completion["choices"][0].message.content
    return res_gpt


def chatgpt_res(messages, data):

    # 사용자의 입력을 메시지로 추가
    usr_ans = {"role": "user", "content": f"내 응답은 <{data}> 야! 제공되지 않은 정보가 있으면 그 부분 번호에 해당하는 질문만 물어봐주고, 채워진 정보는 되묻지 않아도되고, 추가적인 질문이 없으면 찾은 정보를 조합해서 계속 맞냐고 물어봐주세요!!!"}
    messages.append(usr_ans)

    # ChatGPT에게 대화 내용 전달 및 응답 받기
    completion = openai.ChatCompletion.create(
        model=CHAT_GPT_MODEL,
        messages=messages,
        temperature=0
    )
    
    res_gpt = completion["choices"][-1].message.content
    

    # ChatGPT의 응답을 메시지로 추가
    bot_ans = {"role": "assistant", "content": res_gpt}

    return usr_ans ,bot_ans, res_gpt


# 변호사에게 제보해야 하는 제보문 생성
def lawyer_report(data):
    completion = openai.ChatCompletion.create(
        model=CHAT_GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "당신은 교통사고 키워드를 바탕으로 변호사에게 보낼 사연문을 써야하는 임무가 있습니다."
            },
            {
                "role": "user",
                "content": f"당신이 가진 교통사고 키워드는 <{data}>이고, 이 키워드를 바탕으로 호소력있는 사연문을 작성해 주세요"
            },
            {
                "role": "user",
                "content": "중요: 누가 읽더라도 쉽고, 간결하게 호소력있어야 합니다."
            },
        ],
        temperature=1
    )
    # 결과 응답
    res = completion["choices"][0].message.content
    return res