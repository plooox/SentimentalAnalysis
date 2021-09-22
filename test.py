import pandas as pd
import numpy as np
import csv


def load_data():
    data = pd.read_csv("son_summary.csv")
    return


son = pd.read_csv("son_summary.csv")
print([son['positive'], son['negative']])

dataList = np.array(
    [son['positive'].tolist(), son['negative'].tolist()]).transpose()

chart_data = pd.DataFrame(dataList, index = son['date'].tolist(), columns=['pos', 'neg'])
print(chart_data)