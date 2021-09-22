import pandas as pd
import numpy as np
import csv
import datetime

from pandas.core.indexes.datetimes import DatetimeIndex

son = pd.read_csv("./son.csv")
#son['Date'] = son['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d %H:%M:%S'))

#son_date = pd.to_datetime(son["Date"][0])
#print(son_date)

csvFile = open("son_summary.csv", "w", newline='', encoding='utf-8')
csvWrite = csv.writer(csvFile)
csvWrite.writerow(['date', 'positive', 'negative'])
csvFile.close()

prevDate = son["Date"][0].split(' ')[0][:-3]
print(prevDate)
posNum = 0
negNum = 0

for i, row in son.iterrows():
    curDate = row["Date"].split(' ')[0][:-3]
    #print(prevDate + " vs " +curDate)
    if(curDate == prevDate):
        if(row["Pos/Neg"] == 0):
            negNum += 1
        else:
            posNum += 1
    else:
        print(prevDate + ": " + str(posNum)+ " / "+str(negNum))
        csvFile = open("son_summary.csv", "a", newline='', encoding='utf=8')
        csvWrite = csv.writer(csvFile)
        csvWrite.writerow([prevDate, posNum, negNum])
        csvFile.close()

        prevDate = curDate
        negNum = 0
        posNum = 0

        if(row["Pos/Neg"] == '0'):
            negNum += 1
        else:
            posNum += 1

csvFile = open("son_summary.csv", "a", newline='', encoding='utf=8')
csvWrite = csv.writer(csvFile)
csvWrite.writerow([prevDate, posNum, negNum])
csvFile.close()
