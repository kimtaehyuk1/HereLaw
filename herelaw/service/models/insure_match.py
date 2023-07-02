import pandas as pd


# 보험사 데이터 받아오기
def read_insure_data():
    insure_data_path = "herelaw/service/data/insure_match_data.xlsx"

    insure_data = pd.read_excel(insure_data_path, header=0)

    return insure_data


insure_data = read_insure_data()


# 사용자가 입력한 보험사 이름을 이용해서 보험사 데이터 받아오기
def insure_data_matching(insure_name):
    """_summary_

    Args:
        insure_name (str): 사용자가 사용하는 보험사 이름 (ex. "현대해상")

    Returns:
        dict: {'insure_name': 사용자가 사용하는 보험사 이름, 'call': '보험사 전화번호'}
            (ex. {'insure_name': '현대해상', 'call': '1588-5656'})
    """
    # 원하는 데이터 값 추출
    data = insure_data[insure_data["insure_name"] == insure_name]

    # 데이터의 컬럼을 이용해 딕셔너리 형태로 데이터 정리하기
    result = {}
    data_cols = data.columns

    for data_col in data_cols:
        result[data_col] = data[data_col].item()

    return result


if __name__ == "__main__":
    print(insure_data_matching("현대해상"))
