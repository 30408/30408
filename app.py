import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# ✅ 한글 폰트 설정 (Windows 기준)
# 그래프에서 한글이 깨지지 않고 제대로 표시되도록 폰트를 설정합니다.
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  
# 마이너스(-) 기호가 깨지지 않도록 설정
plt.rcParams['axes.unicode_minus'] = False  

# Streamlit 페이지 기본 설정
# 페이지 제목과 레이아웃(와이드 모드) 설정
st.set_page_config(page_title="생물성 연소 배출량 분석", layout="wide")

# 웹앱 메인 제목 출력
st.title("🚗 지역별 생물성 연소 배출량 분석")

# ✅ CSV 파일 경로 설정
# data 폴더 안에 있는 CSV 파일을 불러옵니다.
csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")

try:
    # CSV 파일 읽기 (encoding='cp949'는 한글이 포함된 파일에 주로 사용)
    df = pd.read_csv(csv_path, encoding="cp949")
    # 성공 메시지 출력
    st.success("CSV 파일을 성공적으로 불러왔습니다!")
    # 불러온 데이터 표 형태로 보여주기
    st.dataframe(df)
except Exception as e:
    # 파일을 읽는데 실패하면 에러 메시지 출력 후 실행 중단
    st.error("CSV 파일을 불러오는 데 문제가 발생했습니다.")
    st.exception(e)
    st.stop()

# ✅ 열 이름 정리
# 첫 번째 열 이름을 '구분(1)'로 변경 (원본 컬럼명이 긴 경우 간단하게 바꿈)
df = df.rename(columns={df.columns[0]: '구분(1)'})

# '구분(1)' 열에서 같은 제목이 반복된 행(제목 행 등) 삭제
df = df[df['구분(1)'] != '구분(1)']

# ✅ '생물성 연소' 열 데이터 숫자형으로 변환
# 쉼표(,)를 제거하고 숫자로 변환 (예: "1,234" -> 1234)
df['생물성 연소'] = df['생물성 연소'].astype(str).str.replace(",", "")
df['생물성 연소'] = pd.to_numeric(df['생물성 연소'], errors='coerce')

# --------- 1. 지역별 전체 생물성 연소 배출량 순위 ---------
st.header("📍 지역별 전체 생물성 연소 배출량 순위")

# '구분(1)'과 '생물성 연소' 열만 선택하고 NaN 값 제거 후 배출량 기준 내림차순 정렬
region_df = df[['구분(1)', '생물성 연소']].dropna().sort_values(by='생물성 연소', ascending=False)

# 정렬된 표를 웹앱에 보여주기
st.dataframe(region_df.reset_index(drop=True), use_container_width=True)

# 상위 10개 지역만 따로 추출
top10_region = region_df.head(10)

# 그래프 그리기 (막대그래프)
fig1, ax1 = plt.subplots()
ax1.bar(top10_region['구분(1)'], top10_region['생물성 연소'], color='skyblue')
ax1.set_title("상위 10개 지역의 생물성 연소 배출량")
ax1.set_ylabel("배출량 (t)")  # 단위는 톤(t)
plt.xticks(rotation=45)  # x축 라벨을 45도 기울여서 글자가 겹치지 않도록 함
st.pyplot(fig1)  # 그래프를 Streamlit에 출력

# --------- 2. 각 지역별 최다 연소 종류 분석 ---------
st.header("🔥 지역별로 가장 많이 배출한 연소 종류")

# '연소 종류' 컬럼 이름들 추출 ('구분(1)' 제외)
category_columns = df.columns.drop('구분(1)')

region_max_category = []

# 각 행(지역)별로 최다 배출 연소 종류를 찾기 위한 반복문
for idx, row in df.iterrows():
    region = row['구분(1)']  # 지역명
    
    # 각 연소 종류 컬럼의 값을 쉼표 제거 후 숫자로 변환
    category_values = row[category_columns].apply(
        lambda x: pd.to_numeric(str(x).replace(",", ""), errors='coerce')
    )
    
    # 값이 모두 NaN인 경우 건너뜀
    if category_values.dropna().empty:
        continue

    # 가장 큰 값(최다 배출량)을 가진 연소 종류와 값 추출
    max_col = category_values.idxmax()
    max_value = category_values[max_col]
    
    # 결과 리스트에 딕셔너리 형태로 저장
    region_max_category.append({
        "지역": region,
        "가장 많이 배출한 연소 종류": max_col,
        "배출량 (t)": max_value
    })

# 리스트를 데이터프레임으로 변환
region_max_df = pd.DataFrame(region_max_category)

# 배출량 기준 내림차순 정렬
region_max_df = region_max_df.sort_values(by="배출량 (t)", ascending=False)

# 정리된 표를 웹앱에 보여주기
st.dataframe(region_max_df.reset_index(drop=True), use_container_width=True)

# 상위 10개 지역만 따로 추출하여 시각화
top10_max = region_max_df.head(10)

fig3, ax3 = plt.subplots(figsize=(10, 5))
bars = ax3.bar(top10_max['지역'], top10_max['배출량 (t)'], color='mediumseagreen')

ax3.set_title("지역별 최다 배출 연소 종류 (상위 10개)")
ax3.set_ylabel("배출량 (t)")

plt.xticks(rotation=45)  # x축 라벨 각도 조정

# 각 막대 위에 최다 배출 연소 종류 이름을 텍스트로 표시
for bar, label in zip(bars, top10_max['가장 많이 배출한 연소 종류']):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, height, label, 
             ha='center', va='bottom', fontsize=8, rotation=45)

# 그래프를 Streamlit에 출력
st.pyplot(fig3)


