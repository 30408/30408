import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# ✅ 한글 폰트 설정 (Windows 기준. Mac이나 Linux는 다르게 해야 함)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

st.set_page_config(page_title="생물성 연소 배출량 분석", layout="wide")
st.title("🚗 지역별 생물성 연소 배출량 분석")

# ✅ 고정된 경로의 CSV 불러오기
csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")

try:
    df = pd.read_csv(csv_path, encoding="cp949")
    st.success("CSV 파일을 성공적으로 불러왔습니다!")
    st.dataframe(df)
except Exception as e:
    st.error("CSV 파일을 불러오는 데 문제가 발생했습니다.")
    st.exception(e)
    st.stop()

# ✅ 열 이름 정리
df = df.rename(columns={df.columns[0]: '구분(1)'})
df = df[df['구분(1)'] != '구분(1)']  # 제목 행 제거

# ✅ '2022.9' 숫자형으로 변환 (쉼표 제거 후 float으로)
df['생물성 연소'] = df['생물성 연소'].astype(str).str.replace(",", "")
df['생물성 연소'] = pd.to_numeric(df['생물성 연소'], errors='coerce')

# --------- 1. 지역별 분석 ---------
st.header("📍 지역별 전체 생물성 연소 배출량 순위")

region_df = df[['구분(1)', '생물성 연소']].dropna().sort_values(by='생물성 연소', ascending=False)
st.dataframe(region_df.reset_index(drop=True), use_container_width=True)

top10_region = region_df.head(10)
fig1, ax1 = plt.subplots()
ax1.bar(top10_region['구분(1)'], top10_region['생물성 연소'], color='skyblue')
ax1.set_title("상위 10개 지역의 생물성 연소 배출량")
ax1.set_ylabel("배출량 (t)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# --------- 2. 각 지역별 최다 연소 종류 분석 ---------
st.header("🔥 지역별로 가장 많이 배출한 연소 종류")

# NaN 제거
region_max_category = []

for idx, row in df.iterrows():
    region = row['구분(1)']
    category_values = row[category_columns]
    max_col = category_values.idxmax()
    max_value = category_values[max_col]
    region_max_category.append({
        "구분(1)": region,
        "가장 많이 배출한 연소 종류": max_col,
        "배출량 (t)": max_value
    })

region_max_df = pd.DataFrame(region_max_category)
region_max_df = region_max_df.sort_values(by="배출량 (t)", ascending=False)

st.dataframe(region_max_df.reset_index(drop=True), use_container_width=True)

# 상위 10개 지역만 시각화
top10_max = region_max_df.head(10)
fig3, ax3 = plt.subplots(figsize=(10, 5))
bars = ax3.bar(top10_max['구분(1)'], top10_max['배출량 (t)'], color='mediumseagreen')
ax3.set_title("지역별 최다 배출 연소 종류 (상위 10개)")
ax3.set_ylabel("배출량 (t)")
plt.xticks(rotation=45)

# 각 막대 위에 연소 종류 이름 표시
for bar, label in zip(bars, top10_max['가장 많이 배출한 연소 종류']):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, height, label, ha='center', va='bottom', fontsize=8, rotation=45)

st.pyplot(fig3)

