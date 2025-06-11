import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CO 배출량 분석", layout="wide")

st.title("🚗 지역별 및 연소 종류별 CO 배출량 분석")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded_file)

    # 첫 번째 열 이름을 '지역'으로 변경
    df = df.rename(columns={df.columns[0]: '지역'})

    # --------- 1. 지역별 배출량 분석 ---------
    st.header("📍 지역별 전체 CO 배출량 순위")

    region_df = df[['지역', '배출원대분류 합계']].sort_values(by='배출원대분류 합계', ascending=False)

    st.dataframe(region_df.reset_index(drop=True), use_container_width=True)

    # 막대 그래프 (상위 10개 지역)
    top10_region = region_df.head(10)
    fig1, ax1 = plt.subplots()
    ax1.bar(top10_region['지역'], top10_region['배출원대분류 합계'], color='skyblue')
    ax1.set_title("상위 10개 지역의 CO 배출량")
    ax1.set_ylabel("배출량 (t)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # --------- 2. 연소 종류별 배출량 분석 ---------
    st.header("🔥 연소 종류별 전체 CO 배출량 순위")

    # '지역'과 '배출원대분류 합계'를 제외한 연소 종류 컬럼 합산
    category_columns = df.columns[2:]
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

