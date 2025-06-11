import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 페이지 설정은 최상단, 첫 번째 Streamlit 명령어로!
st.set_page_config(page_title="CO 배출량 분석", layout="wide")

st.title("🚗 지역별 및 연소 종류별 CO 배출량 분석")

# 파일 경로 지정 (실제 경로에 맞게 수정)
csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")

# CSV 불러오기 (인코딩 문제 해결)
try:
    df = pd.read_csv(csv_path, encoding="cp949")
    st.success("CSV 파일을 성공적으로 불러왔습니다!")
    st.dataframe(df)
except Exception as e:
    st.error("CSV 파일을 불러오는 데 문제가 발생했습니다.")
    st.exception(e)
    st.stop()  # 에러 발생 시 이후 실행 중단

# 열 이름 정리
df = df.rename(columns={df.columns[0]: '구분(1)'})

# '구분(1)' 컬럼에서 제목 행 제거 (만약 헤더가 2중으로 들어간 경우)
df = df[df['구분(1)'] != '구분(1)']

# --------- 1. 지역별 배출량 분석 ---------
st.header("📍 지역별 전체 CO 배출량 순위")

# 지역별 총합 기준 정렬
region_df = df[['구분(1)', '2022']].sort_values(by='2022', ascending=False)

st.dataframe(region_df.reset_index(drop=True), use_container_width=True)

# 막대 그래프 (상위 10개 지역)
top10_region = region_df.head(10)
fig1, ax1 = plt.subplots()
ax1.bar(top10_region['구분(1)'], top10_region['2022'], color='skyblue')
ax1.set_title("상위 10개 지역의 CO 배출량")
ax1.set_ylabel("배출량 (t)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# --------- 2. 연소 종류별 배출량 분석 ---------
st.header("🔥 연소 종류별 전체 CO 배출량 순위")

# 연소 항목만 추출
category_columns = df.columns.drop(['구분(1)', '2022'])
category_sum = df[category_columns].sum().sort_values(ascending=False)

category_df = pd.DataFrame({
    "연소 종류": category_sum.index,
    "총 배출량": category_sum.values
})

st.dataframe(category_df.reset_index(drop=True), use_container_width=True)

# 막대 그래프
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(category_sum.index, category_sum.values, color='salmon')
ax2.set_title("연소 종류별 총 CO 배출량")
ax2.set_ylabel("배출량 (t)")
plt.xticks(rotation=45)
st.pyplot(fig2)


