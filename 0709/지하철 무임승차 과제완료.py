#!/usr/bin/env python
# coding: utf-8

# In[145]:


from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests


### 사용자가 원하는 url 생성 함수
def url_print(tdate, uRow=5):
    uKey = "4b50664d47646c6731303950545a7466"
    url_gibon="http://openapi.seoul.go.kr:8088/" + uKey
    url_obj="/xml/CardSubwayPayFree/"
    url_row="1/"+ str(uRow) +"/"
    url_date=tdate[:6]
    url=url_gibon+url_obj+url_row+url_date

    url_soup=html_parser(url)

    return url_soup


### url을 이용한 웹 사이트 파씽
def html_parser(url):
    url_xml = requests.get(url)
    if url_xml.status_code != 200:
        print('데이터를 가져오지 못했습니다.')
        exit()
    soup = bs(url_xml.content, 'html.parser')
    return soup


### 딕셔너리 구조로 저장 후 DataFarame 구조로 변경
def seoul_sw_pandas(seoul_sw_soup):
    xml_row = seoul_sw_soup.find_all('row')
    xml_txt = []
    for row in xml_row:
        dt = row.find('use_mon').text               
        line = row.find('line_num').text           
        sub_sta = row.find('sub_sta_nm').text      
        payride = row.find('pay_ride_num').text     
        freeride = row.find('free_ride_num').text
        payalight = row.find('pay_alight_num').text 
        freealight = row.find('free_alight_num').text 


        xml_txt.append({'사용월': dt, '호선명': line, '지하철명': sub_sta, '유임 승차 인원': payride, '무임 승차 인원': freeride ,
                        '유임하차인원':payalight ,'무임하차인원':freealight })

    #print(xml_txt)
    df = pd.DataFrame(xml_txt)
    return df


# 시작일부터 종료일까지의 날짜문자 리스트를 이용해 전체 일자별 데이터 조회 pandas.concat()을 이용한 행추가
def main_api(sDt, eDt):
    # pd.date_range(start=staDate, end=endDate) : 시작일부터 종료일까지 날짜 생성, 시작일/종료일=>문자형
    dt_index = pd.date_range(start=sDt, end=eDt)
    dtList = dt_index.strftime("%Y%m").tolist()  # 날짜형을 문자형으로 변경후 리스트형으로 저장
    mon_lst=[]
    for i in range(len(dtList)-1):
        if len(mon_lst)==0:
            mon_lst.append(dtList[i])
        elif dtList[i]!=dtList[i+1]:
            mon_lst.append(dtList[i+1])
    df0 = pd.DataFrame()  # 전체 데이터 저장 변수
    for sDt in tqdm(mon_lst, desc="진행율: "):
        seoul_sw_soup = url_print(sDt)  # 한페이지에 5개의 데이터가 출력된 url 정보 가져오기
        uRow = seoul_sw_soup.find('list_total_count').text  # 조회된 전체 데이터 개수 추출하기
        seoul_sw_soup = url_print(sDt, uRow)  # 한페이지에 추출한 전체 데이터 출력 url 정보 가져오기
        df = seoul_sw_pandas(seoul_sw_soup)  # 요청 데이터에 대한 DataFrame 형식으로 변경하기

        df0 = pd.concat([df0, df], ignore_index=True)  # ignore_index=True: 인덱스 재배열(재설정)

    return df0


sDt=input('시작날짜 입력(예 20150507): ')
eDt=input('종료날짜 입력(예 20170609): ')

df0=main_api(sDt, eDt)
print(df0)



# In[134]:


sDt='20200101'
eDt='20200202'

dt_index = pd.date_range(start=sDt, end=eDt)
dtList = dt_index.strftime("%Y%m").tolist()  # 날짜형을 문자형으로 변경후 리스트형으로 저장
mon_lst=[]
for i in range(len(dtList)-1):
    if len(mon_lst)==0:
        mon_lst.append(dtList[i])
    elif dtList[i]!=dtList[i+1]:
        mon_lst.append(dtList[i+1])

        
print(mon_lst)


# In[142]:


sDt='20200101'
eDt='20200305'

dt_index = pd.date_range(start=sDt, end=eDt)
dtList = dt_index.strftime("%Y%m").tolist()  # 날짜형을 문자형으로 변경후 리스트형으로 저장
mon_lst=[]
for i in range(len(dtList)-1):
    if len(mon_lst)==0:
        mon_lst.append(dtList[i])
    elif dtList[i]!=dtList[i+1]:
        mon_lst.append(dtList[i+1])
df0 = pd.DataFrame()  # 전체 데이터 저장 변수
for sDt in tqdm(mon_lst, desc="진행율: "):
    seoul_sw_soup = url_print(sDt)  # 한페이지에 5개의 데이터가 출력된 url 정보 가져오기
    uRow = seoul_sw_soup.find('list_total_count').text  # 조회된 전체 데이터 개수 추출하기
    seoul_sw_soup = url_print(sDt, uRow)  # 한페이지에 추출한 전체 데이터 출력 url 정보 가져오기
    df = seoul_sw_pandas(seoul_sw_soup)  # 요청 데이터에 대한 DataFrame 형식으로 변경하기

    df0 = pd.concat([df0, df], ignore_index=True)  # ignore_index=True: 인덱스 재배열(재설정)


print(df0.info)
        

    
    


# In[ ]:




