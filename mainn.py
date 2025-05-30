import pandas as pd
import folium

# CSV나 DataFrame 형식으로 되어 있다고 가정
data = pd.read_csv("your_data.csv")  # 또는 직접 DataFrame 생성

# 평균 위치를 중심으로 지도 생성
center_lat = data['Latitude'].mean()
center_lon = data['Longitude'].mean()
map_ = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 데이터 포인트를 지도에 표시
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color='blue',
        fill=True,
        fill_opacity=0.7
    ).add_to(map_)

# 지도 출력 (Jupyter Notebook 사용 시)
map_
# 또는 저장
map_.save("map.html")

