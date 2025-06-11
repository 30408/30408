import pandas as pd

# CSV 파일 읽기 (파일 경로가 정확해야 함)
df = pd.read_csv("일산화탄소_CO__배출량_20250609093209.csv")

# 데이터 확인
print(df.head())
