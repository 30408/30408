import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

st.title("📍 배송 위치 기반 군집 분석 (Folium 지도 시각화)")

# CSV 파일 로드 (같은 폴더에 Delivery.csv 있어야 함)
@st.cache_data
def load_data():
    return pd.read_csv("Delivery.csv")

df = load_data()

st.subheader("데이터 미리보기")
st.dataframe(df)

# 위치 컬럼명 지정
lat_col = "Latitude"
lon_col = "Longitude"

if lat_col not in df.columns or lon_col not in df.columns:
    st.error("CSV 파일에 'Latitude'와 'Longitude' 컬럼이 반드시 포함되어야 합니다.")
    st.stop()

# 군집 수 입력받기
st.sidebar.header("군집 분석 설정")
n_clusters = st.sidebar.slider("군집 수 (K)", min_value=2, max_value=10, value=3)

# 위치 데이터만 추출 (결측치 제거)
location_df = df[[lat_col, lon_col]].dropna()

# 데이터 표준화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(location_df)

# KMeans 군집화
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

location_df = location_df.copy()
location_df["Cluster"] = clusters

# 중심 좌표 계산 (지도 초기 위치)
center_lat = location_df[lat_col].mean()
center_lon = location_df[lon_col].mean()

# Folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

# 군집별 색상 리스트
cluster_colors = [
    "red", "blue", "green", "purple", "orange",
    "darkred", "lightblue", "pink", "gray", "cadetblue"
]

# 각 군집에 해당하는 좌표 마커로 추가
for _, row in location_df.iterrows():
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=6,
        color=cluster_colors[int(row["Cluster"]) % len(cluster_colors)],
        fill=True,
        fill_opacity=0.7,
        popup=f"Cluster {row['Cluster']}"
    ).add_to(m)

st.subheader("군집 결과 지도")
st_folium(m, width=700, height=500)
