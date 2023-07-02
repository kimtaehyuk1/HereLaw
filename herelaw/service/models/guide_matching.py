import pandas as pd


# 보험사 데이터 받아오기
def read_guide_data():
    guide_data_path = "herelaw/service/data/guide_match_data.xlsx"

    guide_data = pd.read_excel(guide_data_path, header=0)

    return guide_data


guide_data = read_guide_data()


# 이름에서 확장자 제거
def fault_name_parser(fault_name):
    return fault_name[:-4] if fault_name[-4:] == ".txt" else fault_name


# 사용자가 입력한 결과 데이터의 제목을 이용해서 가이드 데이터 받아오기
def guide_data_matching(fault_name):
    """_summary_

    Args:
        fault_name (str): 사용자의 과실비율 데이터 이름 (ex. "fault_rate_15.txt")

    Returns:
        str: 대응 가이드
    """
    # 과실 이름에서 확장자 제거
    fault_name = fault_name_parser(fault_name)

    # 원하는 데이터 값 추출
    data = guide_data[guide_data["fault_rate"] == fault_name]

    react_name = data["react_guide"].values[0]
    with open(f"herelaw/service/data/guide/{react_name}.txt", "r") as f:
        result = f.read()
    return result


if __name__ == "__main__":
    print(guide_data_matching("fault_rate_15.txt"))
