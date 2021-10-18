from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from krwordrank.sentence import summarize_with_sentences
import pickle
from PIL import Image

@st.cache
def load_data(option):
    data = pd.read_csv("./data/"+option+".csv")
    return data

def setData(option):
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

    with open("./data/keywords/"+option+".pkl", 'rb') as file:
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
    keywords = list(keywords.keys())[:7]
    totalLabel = 'negative','positive'
    totalSize = [totalNeg, totalPos]
    pieFig, pieAxis = plt.subplots()
    pieAxis.pie(totalSize, labels=totalLabel, startangle=90)
    pieAxis.axis('equal')

    return keywords, pieFig, resData

st.header("Sentimental Analysis")
keywordList = pd.read_csv("./keywordList.csv")

option = st.text_input("Enter the keyword")
plist = keywordList['name'].values.tolist()

if option :
    if option in plist:
        keywords, pieFig, resData = setData(option)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Keywords")
            for keyword in keywords:
                st.markdown('- '+keyword)
        with col2:
            st.subheader("Total")
            st.pyplot(pieFig)
        st.subheader("Trends about "+option)
        st.line_chart(resData)
    else:
        st.subheader("아직 분석 결과가 제공되지 않습니다.")
        btn = st.empty()
        if btn.button("분석 요청"):
            requestData = set()
            with open("./request.pkl", 'rb') as file:
                requestData = pickle.load(file)
            requestData.add(option)
            with open("./request.pkl", 'wb') as file:
                pickle.dump(requestData,file)
            btn.text("submit!")
else:
    col1, col2 = st.columns(2)
    c1Image = Image.open('./test.png')
    c2Image = Image.open('./test2.png')
    with col1:
        st.subheader("키워드를 검색하세요")
        st.image(c1Image)
    with col2:
        st.subheader("분석결과")
        st.image(c2Image)