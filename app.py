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

