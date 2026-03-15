import streamlit as st 
import pandas as pd

st.title("AI News Dashboard")

df = pd.read_csv("data/final.csv")

st.write("Latest News")

st.dataframe(df)

st.subheader("Titles")

for i, row in df.iterrows():
    st.write(row["title"])
    st.write(row["url"])
