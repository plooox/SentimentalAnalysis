from os import altsep, curdir
import pandas as pd
from pandas.core.indexes.base import Index
import numpy as np

personalData = pd.read_csv("./손흥민.csv")

newData = pd.DataFrame({"date":"0000-00","positive":[0],"negative":[0]})
# newData = newData.append({"date":"1111-11","positive":1,"negative":1}, ignore_index=True)
totalPos = 0
totalNeg = 0
pos = 0
neg = 0
prevDate = "0000-00"


for idx, rowData in personalData.iterrows():
    # print(rowData)
    curDate = rowData["Date"].split(' ')[0][:-3]

    if(curDate != prevDate):
        newData = newData.append({"date":prevDate,"positive":pos,"negative":neg}, ignore_index=True)
        totalPos += pos
        totalNeg += neg
        neg = 0
        pos = 0
        prevDate = curDate
        
        if(rowData["Pos/Neg"] == 1):
            pos +=  1
        else:
            neg += 1

    else:
        if(rowData["Pos/Neg"] == 1):
            pos +=  1
        else:
            neg += 1

newData = newData.append({"date":prevDate,"positive":pos,"negative":neg}, ignore_index=True)

newData = newData.set_index('date')
resData = newData.drop(['0000-00'])
        
print("===============================")
cmpData = pd.read_csv("./son_data.csv")
dataList = np.array([cmpData['positive'].tolist(), cmpData['negative'].tolist()]).transpose()
res_data = pd.DataFrame(
    dataList, index=cmpData['date'].tolist(), columns=['pos', 'neg'])

print(cmpData)
print("===============================")
print(res_data)
totalData = pd.DataFrame(np.array([totalPos,totalNeg]),columns=['number of data'],index=['positive','negative'])
print(totalData)