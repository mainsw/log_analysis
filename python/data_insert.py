import pandas as pd
import mysql.connector

# MySQL 연결 설정
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'db',
    'raise_on_warnings': True
}

# MySQL 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 인덱스 및 제약 조건 비활성화
# cursor.execute("ALTER TABLE traffic_data ...")  # 필요에 따라

# 트랜잭션 시작
cursor.execute("START TRANSACTION")

# CSV 파일을 청크로 나누어 읽기
chunk_size = 500000  # 예: 5만 행씩 처리
total_rows_processed = 0

for chunk in pd.read_csv('.\\output\\chunk_13.csv', chunksize=chunk_size):
    # 데이터 삽입 쿼리 생성
    data_tuples = [tuple(row) for index, row in chunk.iterrows()]
    insert_query = "INSERT INTO traffic_data (seq, epochtime, id_num, src_ip, src_mac, src_port, dest_ip, dest_mac, dest_port, size_kb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, data_tuples)
    
    # 진행 상황 업데이트 및 출력
    total_rows_processed += len(chunk)
    print(f"Processed {total_rows_processed} rows so far...")


# 트랜잭션 커밋
cursor.execute("COMMIT")

# 인덱스 및 제약 조건 다시 활성화
# cursor.execute("ALTER TABLE traffic_data ...")  # 필요에 따라

# 연결 종료
cursor.close()
conn.close()
