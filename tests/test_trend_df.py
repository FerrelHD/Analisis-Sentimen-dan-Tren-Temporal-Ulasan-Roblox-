
import pandas as pd
import os

df = pd.read_csv("data/processed/sentiment_comparison_full.csv")
df['at'] = pd.to_datetime(df['at'], errors='coerce')
df['sentiment_indobert'] = df['sentiment_after'].fillna('').astype(str).str.strip().str.lower()
label_ui = {'positif': 'Positif', 'netral': 'Netral', 'negatif': 'Negatif'}
df['sentiment_ui_ts'] = df['sentiment_indobert'].map(label_ui)

trend_df = df.groupby([df['at'].dt.date, 'sentiment_ui_ts']).size().reset_index(name='count')
print("trend_df info:")
print(trend_df.head(20))
print("\nNumber of unique dates in trend_df:", trend_df['at'].nunique())
print("\nAll unique at values sorted:", sorted(trend_df['at'].unique()))

