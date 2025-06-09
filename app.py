import streamlit as st
import pandas as pd

st.title("지역별 일산화탄소(CO) 배출량 분석 대시보드")

@st.cache_data
def load_data():
    df = pd.read_csv("data/일산화탄소_CO__배출량.csv", encoding='cp949')
    df.columns = df.iloc[0]  # 첫 행을 열 이름으로
    df = df.drop(0).reset_index(drop=True)  # 첫 행 제거
    return df

df = load_data()

st.subheader("원본 데이터 미리보기")
st.dataframe(df)
