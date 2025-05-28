import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Plotly 시각화", layout="centered")
st.title("📊 Google Drive CSV Plotly 시각화 웹앱")

# 1. Google Drive에서 CSV 불러오기
url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"
try:
    df = pd.read_csv(url)
    st.success("✅ 데이터 불러오기 성공")
except Exception as e:
    st.error(f"❌ 데이터 불러오기 실패: {e}")
    st.stop()

# 2. 데이터 구조 확인
st.subheader("데이터 미리보기")
st.dataframe(df)

# 3. 사용자에게 열 선택 받기
numeric_cols = df.select_dtypes(include='number').columns.tolist()
text_cols = df.select_dtypes(include='object').columns.tolist()

if not numeric_cols or not text_cols:
    st.warning("📛 시각화를 위한 텍스트 또는 숫자형 열이 부족합니다.")
    st.stop()

x_col = st.selectbox("X축 (문자형 열 선택)", text_cols)
y_col = st.selectbox("Y축 (숫자형 열 선택)", numeric_cols)

# 4. Plotly 시각화
fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
st.plotly_chart(fig)
