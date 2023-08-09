import mysql.connector

# MySQL 연결 설정
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'test',
    'raise_on_warnings': True
}

# MySQL 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 테이블 생성 쿼리
create_table_query = """
CREATE TABLE traffic_data (
    seq INT,
    epochtime BIGINT,
    id_num INT,
    src_ip BIGINT,
    src_mac BIGINT,
    src_port INT,
    dest_ip BIGINT,
    dest_mac BIGINT,
    dest_port INT,
    size_kb INT
);
"""

# 테이블 생성
cursor.execute(create_table_query)

# 연결 종료
cursor.close()
conn.close()