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

# --------- 2. 연소 종류별 분석 ---------
st.header("🔥 연소 종류별 전체 생물성 연소 배출량 순위")

category_columns = df.columns.drop(['구분(1)', '생물성 연소'])
# 쉼표 제거 및 숫자 변환
for col in category_columns:
    df[col] = df[col].astype(str).str.replace(",", "")
    df[col] = pd.to_numeric(df[col], errors='coerce')

category_sum = df[category_columns].sum().sort_values(ascending=False)

category_df = pd.DataFrame({
    "연소 종류": category_sum.index,
    "총 배출량": category_sum.values
})

st.dataframe(category_df.reset_index(drop=True), use_container_width=True)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(category_sum.index, category_sum.values, color='salmon')
ax2.set_title("연소 종류별 총 CO 배출량")
ax2.set_ylabel("배출량 (t)")
plt.xticks(rotation=45)
st.pyplot(fig2)

