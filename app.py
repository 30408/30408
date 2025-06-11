import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV 경로 지정
csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")

# CSV 읽기 (인코딩 오류 방지)
df = pd.read_csv(csv_path, encoding='cp949')

st.title("🌍 지역별 일산화탄소(CO) 배출량 및 연소 종류 분석")

# 지역 목록 생성
regions = df['지역'].unique()
selected_region = st.selectbox("분석할 지역을 선택하세요:", regions)

# 선택한 지역 필터링
region_df = df[df['지역'] == selected_region]

# 지역의 총 CO 배출량 계산
total_emission = region_df['배출량'].sum()
st.metric(label=f"{selected_region}의 총 CO 배출량", value=f"{total_emission:,.2f} 톤")

# 연소 종류별 배출량
grouped_fuel = region_df.groupby('연소종류')['배출량'].sum().sort_values(ascending=False)

# 가장 많이 배출한 연소 종류
most_common_fuel = grouped_fuel.idxmax()
most_common_value = grouped_fuel.max()

st.subheader(f"🔥 {selected_region}에서 가장 많은 CO를 배출한 연소 카테고리:")
st.write(f"→ **{most_common_fuel}**: {most_common_value:,.2f} 톤")

# 막대 그래프 시각화
st.subheader(f"📊 {selected_region}의 연소 종류별 CO 배출량")

fig, ax = plt.subplots()
grouped_fuel.plot(kind='bar', ax=ax, color='teal')
ax.set_ylabel("배출량 (톤)")
ax.set_title(f"{selected_region} - 연소 종류별 일산화탄소 배출량")
st.pyplot(fig)
