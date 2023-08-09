import pandas as pd

input_file = "security2.csv"
output_path = "D:\\완성샘플\\output"
chunk_size = 10000000  # 청크 크기, 1000만개의 행을 갖는 청크로 나누기.

chunk_number = 1
for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    output_file = f"{output_path}/chunk_{chunk_number}.csv"
    chunk.to_csv(output_file, index=False)
    chunk_number += 1
