import streamlit as st
import pandas as pd
import os

# 파일 경로 지정
csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")

# CSV 불러오기 (인코딩 문제 해결)
try:
    df = pd.read_csv(csv_path, encoding="cp949")
    st.success("CSV 파일을 성공적으로 불러왔습니다!")
    st.dataframe(df)
except Exception as e:
    st.error("CSV 파일을 불러오는 데 문제가 발생했습니다.")
    st.exception(e)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV 경로 지정
csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")

# CSV 읽기 (인코딩 오류 방지)
df = pd.read_csv(csv_path, encoding='cp949')

st.title("🌍 지역별 일산화탄소(CO) 배출량 및 연소 종류 분석")

# 지역별 총 배출량 집계 및 내림차순 정렬
total_emission_by_region = df.groupby('구분(1)')['배출량'].sum().sort_values(ascending=False)

st.subheader("🏆 지역별 총 CO 배출량 순위")
st.dataframe(total_emission_by_region.to_frame().rename(columns={'배출량': '총 배출량 (톤)'}))

# 각 지역별로 연소 종류별 배출량 순위 보여주기
for region in total_emission_by_region.index:
    st.markdown(f"---")
    st.subheader(f"📍 {region} - 연소 종류별 CO 배출량 순위")

    region_df = df[df['구분(1)'] == region]
    grouped_fuel = region_df.groupby('연소종류')['배출량'].sum().sort_values(ascending=False)

    # 표 출력
    st.table(grouped_fuel.to_frame().rename(columns={'배출량': '배출량 (톤)'}))

    # 막대 그래프 시각화
    fig, ax = plt.subplots(figsize=(8,4))
    grouped_fuel.plot(kind='bar', ax=ax, color='teal')
    ax.set_ylabel("배출량 (톤)")
    ax.set_title(f"{region} - 연소 종류별 일산화탄소 배출량")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # 값 표시
    for i, v in enumerate(grouped_fuel):
        ax.text(i, v + max(grouped_fuel)*0.01, f"{v:,.0f}", ha='center', fontsize=9)

    st.pyplot(fig)

