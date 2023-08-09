import os
import re

def insert_newlines_in_file(input_file_path, output_file_path, incomplete_log=None):
    # 입력 파일을 읽기 모드로 열기
    with open(input_file_path, 'r') as file:
        logs = file.read()
        
    # 이전 파일에서 미완성된 로그가 있다면 앞에 추가하기
    if incomplete_log:
        logs = incomplete_log + logs

    # 각 로그 라인이 시작되는 패턴 정의
    pattern = r"(\w{3}\s\d{2}\s\d{4}\s\w+\s\d{2}:\d{2}:\d{2})\s(\w+)\s(\d+)\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s([0-9a-fA-F:]{17})\s(\d+)\s(\w+)\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s([0-9a-fA-F:]{17})\s(\d+)\s(\d+)"

    # 모든 패턴 찾기
    matches = re.findall(pattern, logs)
    
    # 마지막으로 찾은 패턴 이후의 문자열 추출
    if matches:
        last_match_end = logs.rfind(matches[-1][-1]) + len(matches[-1][-1])
        incomplete_log = logs[last_match_end:].strip()
    else:
        incomplete_log = logs.strip()

    # 로그를 개행으로 연결하기
    restored_logs = "\n".join([" ".join(log) for log in matches])

    # 출력 파일을 쓰기 모드로 열고 업데이트된 로그 작성
    with open(output_file_path, 'w') as file:
        file.write(restored_logs)

    return incomplete_log

def process_all_files_in_directory(directory):
    # 디렉토리 내의 모든 파일 목록 가져오기
    files = sorted(os.listdir(directory))  # 올바른 순서로 파일 정렬
    incomplete_log = None

    # 파일들을 순회하기
    for file in files:
        # 전체 파일 경로 구성
        input_file = os.path.join(directory, file)
        output_file = os.path.join(directory, file + "_output.txt")

        # 'insert_newlines_in_file' 함수를 사용하여 각 파일 처리
        incomplete_log = insert_newlines_in_file(input_file, output_file, incomplete_log)

    # 모든 파일 처리 후 미완성된 로그가 남아 있으면 필요에 따라 처리하거나 로그로 기록
    if incomplete_log:
        print("경고: 미완성된 로그 발견:", incomplete_log)

# 'log' 디렉토리 내의 모든 파일 처리를 위한 함수 호출
process_all_files_in_directory('log')
