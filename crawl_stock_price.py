import pandas as pd

### krx url에서 회사와 종목코드 데이터를 불러옴.
data = pd.read_html("http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13", header=0)[0]
data.종목코드 = data.종목코드.map('{:06d}'.format)
data = data[['회사명', '종목코드']]

### 네이버 금융에서 주식값을 불러옴.
### 셀트리온 주식코드는 068270

def get_url(firm, data):
    종목코드 = data.query("회사명=='{}'".format(firm))['종목코드'].to_string(index=False).replace(" ", "")
    url = 'http://finance.naver.com/item/sise_day.nhn?code=068270'
    return url

### 셀트리온의 데이터를 불러옴.
firm = '셀트리온'
url = get_url(firm, data)

### 주식값을 보기 좋게 정리함.
stock = pd.DataFrame()

### 1~10 페이지의 데이터를 불러옴.
for page in range(1, 10):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    stock = stock.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

stock = stock.dropna()

### 주식값을int형으로 바꿔줌
stock[['종가','전일비','시가','고가','저가','거래량']] \
    = stock[['종가','전일비','시가','고가','저가','거래량']].astype(int)

### 주식 날짜를 datetime으로 전환후, 오름차순으로 정리해줌.
stock['날짜'] = pd.to_datetime(stock['날짜'])
stock = stock.sort_values(by=['날짜'], ascending=True)

##마지막 5일 간의 주식 값
#stock.head()

##최근 5일 간의 주식 값
#stock.tail()

##데이터를 csv 파일로 전환함.
#stock.to_csv('C:/Users/lemon/Desktop/test.csv', sep=',', na_rep='NaN', encoding='utf-8-sig')
