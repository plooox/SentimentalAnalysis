import streamlit as st
import pandas as pd
import numpy as np

@st.cache
def load_data():
    data = pd.read_csv("son_summary.csv")
    return data

st.title("Trend about Son")

son = load_data()

dataList = np.array([son['positive'].tolist(), son['negative'].tolist()]).transpose()

chart_data = pd.DataFrame(
    dataList, index=son['date'].tolist(), columns=['pos', 'neg'])

st.line_chart(chart_data)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)
