from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.request
import os
from tqdm import tqdm
import time

keyword = input('검색 이미지 검색어를 입력하세요.: ')

url = 'https://www.google.com/search?q=' + keyword
url = url + '&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjWzf6z6ebxAhUAyosBHeqnDHsQ_AUoAXoECAEQAw&biw=958&bih=959'

driver = webdriver.Chrome('c:/pydata/chromedriver.exe')
driver.get(url)
time.sleep(2)

img_url_list = []

for i in range(10):
    if i == 5:
        # 더보기 버튼 클릭
        driver.find_element_by_css_selector(
            "#islmp > div > div > div > div.gBPM8 > div.qvfT1 > div.YstHxe > input").click()
        time.sleep(2)

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
html_source=driver.page_source
soup=bs(html_source, 'html.parser')
img_soup=soup.select('img.rg_i.Q4LuWd')

img_list=[]

for img in tqdm(img_soup, desc="링크 작업"):
    try:
        img_list.append(img['src'])
    except:
        img_list.append(img['data-src'])
fDir = 'c:/pydata/image/'
fName = os.listdir(fDir)
## 중복데이터 제거
print("중복 제거전 사진수:", len(img_list))
img_list=set(img_list)              #중복 제거
print('중복 제거후 사진수',  len(img_list))
### 저장할 폴더존재 여부 확인
fName_dir = keyword
cnt = 0
while True:
    if fName_dir not in fName:
        os.makedirs(fDir + fName_dir)
        break
    cnt += 1
    fName_dir = keyword + str(cnt)
cnt = 0
### 검색 이미지 저장
for img in tqdm(img_list):
    sfdir = fDir + fName_dir + '/' + keyword + str(cnt) + '.jpg'  # 저장 경로와 파일명 설정
    urllib.request.urlretrieve(img, sfdir)  # 이미지 저장하기
    cnt += 1

driver.close()
print('검색 이미지 저장 완료')
