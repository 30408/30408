import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="배송 위치 클러스터링", layout="centered")
st.title("📍 배송 위치 자동 군집 분석 (Folium 지도 시각화)")

# 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Delivery.csv")
        return df
    except FileNotFoundError:
        st.error("❌ 'Delivery.csv' 파일이 현재 디렉토리에 없습니다.")
        st.stop()

df = load_data()

# 위치 컬럼 존재 확인
lat_col, lon_col = "Latitude", "Longitude"
if lat_col not in df.columns or lon_col not in df.columns:
    st.error("❌ 위치 정보가 누락되었습니다 (Latitude / Longitude 필요).")
    st.stop()

st.subheader("📄 데이터 미리보기")
st.dataframe(df.head())

# 사이드바 설정
st.sidebar.header("⚙️ 군집 분석 설정")
n_clusters = st.sidebar.slider("군집 수 (K)", min_value=2, max_value=10, value=3)

# 전처리 및 클러스터링
X = df[[lat_col, lon_col]].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(X_scaled)

X_result = df.loc[X.index].copy()
X_result["Cluster"] = labels

# Folium 지도 생성
center_lat = X_result[lat_col].mean()
center_lon = X_result[lon_col].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

colors = [
    "red", "blue", "green", "purple", "orange",
    "darkred", "lightblue", "pink", "gray", "cadetblue"
]

for _, row in X_result.iterrows():
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=5,
        color=colors[row["Cluster"] % len(colors)],
        fill=True,
        fill_opacity=0.7,
        popup=f"Cluster {row['Cluster']}"
    ).add_to(m)

# 지도 출력
st.subheader("🌍 군집 결과 지도")
st_folium(m, width=700, height=500)
st.write("데이터프레임 컬럼 목록:", df.columns.tolist())
