import streamlit as st
import pandas as pd
import requests
from io import StringIO
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

st.title("📍 배송 위치 자동 군집 분석 (Folium 지도 시각화)")

# 구글 드라이브 링크에서 데이터 불러오기
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1UW9paFlCJMtjK8ct0P_RrG6vU-Dlyrf2"
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    df.columns = [col.strip().lower() for col in df.columns]  # 소문자 통일
    return df

df = load_data()
st.subheader("📄 데이터 미리보기")
st.dataframe(df)

# 컬럼 설정
lat_col = "latitude"
lon_col = "longitude"

if lat_col not in df.columns or lon_col not in df.columns:
    st.error(f"❌ 위치 정보가 누락되었습니다. 현재 컬럼 목록: {df.columns.tolist()}")
    st.stop()

# 사이드바에서 군집 수 설정
st.sidebar.header("⚙️ 군집 분석 설정")
n_clusters = st.sidebar.slider("군집 수 (K)", min_value=2, max_value=10, value=3)

# 군집 분석
X = df[[lat_col, lon_col]].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(X_scaled)
X_result = df.loc[X.index].copy()
X_result["cluster"] = labels

# 지도 시각화
center_lat = X_result[lat_col].mean()
center_lon = X_result[lon_col].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)
colors = ["red", "blue", "green", "purple", "orange", "darkred", "lightblue", "pink", "gray", "cadetblue"]

for _, row in X_result.iterrows():
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=5,
        color=colors[int(row["cluster"]) % len(colors)],
        fill=True,
        fill_opacity=0.7,
        popup=f"Cluster {row['cluster']}"
    ).add_to(m)

st.subheader("🌍 군집 결과 지도")
st_folium(m, width=700, height=500)
