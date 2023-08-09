import csv
import re
from datetime import datetime

# 정규표현식 패턴
pattern = r"(\w{3}\s\d{2}\s\d{4}\s\w+\s\d{2}:\d{2}:\d{2})\s(\w+)\s(\d+)\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s([0-9a-fA-F:]{17})\s(\d+)\s(\w+)\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s([0-9a-fA-F:]{17})\s(\d+)\s(\d+)"

# 변환 함수들
def ip_to_int(ip_str):
    """IP 주소 문자열을 정수 표현으로 변환합니다."""
    segments = ip_str.split('.')
    int_value = 0
    for i, segment in enumerate(reversed(segments)):
        int_value += int(segment) * (256 ** i)
    return int_value

def mac_to_int(mac_str):
    """MAC 주소 문자열을 정수 표현으로 변환합니다."""
    segments = mac_str.split(':')
    int_value = 0
    for i, segment in enumerate(reversed(segments)):
        int_value += int(segment, 16) * (256 ** i)
    return int_value

def process_csv(input_csv_path, output_csv_path, pattern):
    # 입력 CSV 읽기
    with open(input_csv_path, 'r') as infile:
        reader = csv.reader(infile)
        # next(reader)  # 헤더 건너뛰기
        
        csv_data = []
        for row in reader:
            log = " ".join(row)
            match = re.match(pattern, log)
            if match:
                # 날짜와 시간을 epoch로 변환
                dt_str = match.group(1)
                dt_obj = datetime.strptime(dt_str, '%b %d %Y %A %H:%M:%S')
                epoch_time = int(dt_obj.timestamp())
                
                # IP와 MAC 주소를 정수로 변환
                source_ip_int = ip_to_int(match.group(4))
                source_mac_int = mac_to_int(match.group(5))
                dest_ip_int = ip_to_int(match.group(8))
                dest_mac_int = mac_to_int(match.group(9))
                
                # 정규 표현식과 일치하는 부분에서 관련 부분을 추출하고 정수로 변환된 값으로 교체
                relevant_parts = [epoch_time, match.group(3), source_ip_int, source_mac_int, match.group(6), 
                                  match.group(7), dest_ip_int, dest_mac_int, match.group(10), match.group(11)]
                csv_data.append(relevant_parts)
        
        # 처리된 데이터를 출력 CSV에 저장
        with open(output_csv_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['epochtime', 'id_num', 'src_ip', 'src_mac', 'src_port', 
                             'DestName', 'dest_ip', 'dest_mac', 'dest_port', 'size_kb'])
            writer.writerows(csv_data)

process_csv('test.txt', 'processed_logs.csv', pattern)
