import pandas as pd
import datetime
import socket
import struct

# 데이터 로드
data = pd.read_csv('mysql_export.csv')

# 상위 5개 행 확인
data.head()

# epochtime을 datetime으로 변환하는 함수
def epoch_to_datetime(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')

# 정수를 IP 주소 형식으로 변환하는 함수
def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack('!I', ip_int))

# 정수를 MAC 주소 형식으로 변환하는 함수
def int_to_mac(mac_int):
    mac_hex = '{:012x}'.format(mac_int)
    return ':'.join([mac_hex[i:i+2] for i in range(0, 12, 2)])

# 변환 적용
data['epochtime'] = data['epochtime'].apply(epoch_to_datetime)
data['src_ip'] = data['src_ip'].apply(int_to_ip)
data['dest_ip'] = data['dest_ip'].apply(int_to_ip)
data['src_mac'] = data['src_mac'].apply(int_to_mac)
data['dest_mac'] = data['dest_mac'].apply(int_to_mac)

# 변환된 데이터의 상위 5개 행 확인
data.head()

save_path = "converted_data.csv"
data.to_csv(save_path, index=False)