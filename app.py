from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from krwordrank.sentence import summarize_with_sentences
import pickle

# @st.cache
def load_data(option):
    data = pd.read_csv("./data/"+option+".csv")
    return data

def setData(option):
    st.write(option)
    personalData = load_data(option)
    newData = pd.DataFrame({"date":"0000-00","positive":[0],"negative":[0]})
    # newData = newData.append({"date":"1111-11","positive":1,"negative":1}, ignore_index=True)
    totalPos = 0
    totalNeg = 0
    pos = 0
    neg = 0
    prevDate = "0000-00"

    for idx, rowData in personalData.iterrows():
        # print(rowData)
        curDate = rowData["Date"].sㅊplit(' ')[0][:-3]

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

    with open("./data/"+option+".pkl", 'rb') as file:
        twContent = pickle.load(file)

    penalty = lambda x:0 if (25 <= len(x) <= 80) else 1
    stopwords = {option, '출처'}

    keywords, sents = summarize_with_sentences(
        twContent,
        penalty=penalty,
        stopwords = stopwords,
        diversity=0.5,
        num_keywords=100,
        num_keysents=10,
        verbose=False
    )
    topFive = list(keywords.keys())[:5]
    topFiveKeywords = pd.DataFrame(topFive, index={'Top1','Top2','Top3','Top4','Top5'})

    # dataList = np.array([personalData['positive'].tolist(), personalData['negative'].tolist()]).transpose()
    # res_data = pd.DataFrame(
    #     dataList, index=personalData['date'].tolist(), columns=['pos', 'neg'])
    totalLabel = 'positive','negative'
    totalSize = [totalPos, totalNeg]
    pieFig, pieAxis = plt.subplots()
    pieAxis.pie(totalSize, labels=totalLabel, startangle=90)
    pieAxis.axis('equal')

    return topFive, pieFig, resData

option = st.text_input("Enter the keyword")
plist = ['손흥민','이강인','황의조','페이커']

subhead = st.empty()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5")
    btn1 = st.empty()
    btn2 = st.empty()
    btn3 = st.empty()
    btn4 = st.empty()
    btn5 = st.empty()
with col2:
    st.subheader("Total")
    plot = st.empty()
chart = st.empty()


if option :
    if option in plist:
        topFive, pieFig, resData = setData(option)
        clicked = False
        # col1, col2 = col.columns(2)
        if btn1.button(topFive[0], key=topFive[0]+'1'):
            option = topFive[0]
            topFive, pieFig, resData = setData(option)
            clicked = True
        if btn2.button(topFive[1], key=topFive[1]+'2'):
            option = topFive[1]
            topFive, pieFig, resData = setData(option)
            clicked = True
        if btn3.button(topFive[2], key=topFive[2]+'3'):
            option = topFive[2]
            topFive, pieFig, resData = setData(option)
            clicked = True
        if btn4.button(topFive[3], key=topFive[3]+'4'):
            option = topFive[3]
            topFive, pieFig, resData = setData(option)
            clicked = True
        if btn5.button(topFive[4], key=topFive[4]+'5'):
            option = topFive[4]
            topFive, pieFig, resData = setData(option)
            clicked = True
        subhead.subheader("Trends about "+option)
        plot.pyplot(pieFig)
        chart.line_chart(resData)

        if clicked:
            btn1.empty()
            btn2.empty()
            btn3.empty()
            btn4.empty()
            btn5.empty()
            clicked = False
            if btn1.button(topFive[0], key=topFive[0]+'a'):
                option = topFive[0]
                topFive, pieFig, resData = setData(option)
            if btn2.button(topFive[1], key=topFive[1]+'b'):
                option = topFive[1]
                topFive, pieFig, resData = setData(option)
            if btn3.button(topFive[2], key=topFive[2]+'c'):
                option = topFive[2]
                topFive, pieFig, resData = setData(option)
            if btn4.button(topFive[3], key=topFive[3]+'d'):
                option = topFive[3]
                topFive, pieFig, resData = setData(option)
            if btn5.button(topFive[4], key=topFive[4]+'e'):
                option = topFive[4]
                topFive, pieFig, resData = setData(option)
        # with col1:
        #     st.subheader("Top 5 Keywords")
        #     for keyword in topFive:
        #         if btn.button(keyword):
        #             option = keyword
        #             topFive, pieFig, resData = setData(option)
                    
        # with col2:
        #     st.subheader("Total")
        #     st.pyplot(pieFig)
        # st.line_chart(resData)
    else:
        st.write("No data :<")
else:
    st.header("Hello World!")