import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

from pandas import DataFrame

import codecs

### 워드 데이터 열기

## 긍정 데이터 셋
positive = []
## 워드 길이 측정
word = []
file = codecs.open("C:/Users/lemon/Desktop/임시/졸업논문/positive.txt", 'rb', encoding='UTF-8') 

while True: 
    line = file.readline() 
    line = line.replace('\n', '') 
    positive.append(line) 
    word.append(line) 

    if not line: break 
file.close() 

## 부정 데이터 셋
negative = [] 
file2 = codecs.open("C:/Users/lemon/Desktop/임시/졸업논문/negative.txt", 'rb', encoding='UTF-8') 

while True: 
    line = file2.readline() 
    line = line.replace('\n', '') 
    negative.append(line) 
    word.append(line) 

    if not line: break

file2.close()

###주식 값 200개 불러오기
label = [0] * 4000

x = 0
### 추출한 뉴스와 값의 형식
data = {"제목":[], "값":label}

for i in range(400):
    num = i * 10 + 1

    ### 셀트리온 url
    url= "https://search.naver.com/search.naver?where=news&query=%EC%85%80%ED%8A%B8%EB%A6%AC%EC%98%A8&ie=utf8&sm=tab_she&qdt=0" + str(num)
    price = requests.get(url)
    soup = BeautifulSoup(price.text, 'lxml')
    titles = soup.select("a._sp_each_title")

    ### 뉴스 제목 데이터 추출하기
    for title in titles:
        news = title.text
        news = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》]', '', news)
        data['제목'].append(news)

        ### 단어의 길이에서 검토할 길이를  설정함.
        for i in range(len(word)):

            ## flag를 활용하여 분류함.
            p_flag = False
            n_flag = False
            
            if i < (len(positive)-1):
                if news.find(word[i]) != -1:
                    p_flag = True
                    print("긍정,","단어:", word[i],", ", "뉴스제목:", news)
                    break
                
            if i > (len(positive)-2):
                if news.find(word[i]) != -1:
                    n_flag = True
                    print("부정,","단어:", word[i],", ", "뉴스제목:", news)
                    break
                
        ### 긍정일 경우 1       
        if p_flag == True:
            label[x] = 1
            print("postiive",x)
            
        ### 부정일 경우 -1            
        elif n_flag == True:
            label[x] = -1
            print("negative",x)

        ### 긍정도 부정도 아닐 경우 0           
        elif p_flag == False and n_flag == False:
            label[x] = 0
            print("objective",x)

        x = x + 1

###추출한 값 붙이기
data['값'] = label

### 데이터로 전환 후 csv 파일 형식으로 저장함.
dataset = pd.DataFrame(data)
#dataset.to_csv(('C:/Users/lemon/Desktop/data.csv'), sep=',', na_rep='NaN', encoding='utf-8-sig')









