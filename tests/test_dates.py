
import pandas as pd
import os

df = pd.read_csv("data/processed/sentiment_comparison_full.csv")
df['at'] = pd.to_datetime(df['at'], errors='coerce')
df['month_year'] = df['at'].dt.strftime('%B %Y')
print("Unique month_year values:")
print(df['month_year'].value_counts())
print("\nSample dates:")
print(df[['at', 'month_year']].sample(10))

