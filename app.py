import os
import pandas as pd

csv_path = os.path.join("data", "일산화탄소_CO__배출량_20250609093209.csv")
df = pd.read_csv(csv_path)
