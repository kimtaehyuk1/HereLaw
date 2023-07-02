import pymysql as my
from service.config import *


def connect_db():
    try:
        db = my.connect(
            host=DB_HOST_NAME,
            port=DB_PORT,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            charset=DB_CHARSET,
        )
    except Exception as e:
        print(e)
        exit(1)

    return db


# 들어갈것이라 예상되는 데이터:
# 날씨, 사용자 아이디, 과실 비율, 도표 이름, 과실 가이드, 유사판례, 보험사 정보, 사용자 입력 쿼리
def create_table(db, cur):
    # 테이블이 없다면 테이블 생성
    create_table_query = f""" 
    create table if not exists {DB_TABLE_NAME}(
        user_id varchar(255) not null PRIMARY KEY,
        query TEXT not null,
        rate varchar(255) not null,
        rate_name varchar(255) not null,
        law_name varchar(255) not null
    );
    """
    cur.execute(create_table_query)
    db.commit()

    return 0


# 테이블에 담겨있는 모든 데이터 출력
def show_table():
    with connect_db() as db:
        with db.cursor() as cur:
            # 테이블이 없을경우 테이블 생성
            create_table(db, cur)

            # 테이블 확인
            cur.execute(f"SELECT * FROM {DB_TABLE_NAME}")
            rows = cur.fetchall()

    return rows


# 사용자의 로그를 저장
def insert_log(
    user_id, query, rate, rate_name, law_name
):
    with connect_db() as db:
        with db.cursor() as cur:
            # 테이블이 없을경우 테이블 생성
            create_table(db, cur)

            insert_query = f"""insert into {DB_TABLE_NAME}
            values ('{user_id}', "{query}",'{rate}', '{rate_name}','{law_name}');
            """
            cur.execute(insert_query)
            db.commit()

    return 0


if __name__ == "__main__":
    print(show_table())
    insert_log(
        user_id=1234,
        query="안녕하세요",
        rate="0:100",
        rate_name="fault_rate__8000.txt",
        law_name="law_asdasd_8000.txt",
    )
    print(show_table())
