from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.request
import os
from tqdm import tqdm
import time

keyword = input('검색 이미지 검색어를 입력하세요.: ')

url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + keyword

driver = webdriver.Chrome('c:/pydata/chromedriver.exe')
driver.get(url)
time.sleep(2)

img_url_list = []

for i in range(5):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
html_source = driver.page_source
soup = bs(html_source, 'html.parser')
img_soup = soup.select('img._image._listImage')
img_list = []

for img in tqdm(img_soup, desc="링크 작업"):
    img_list.append(img['src'])

fDir = 'c:/pydata/image/'
fName = os.listdir(fDir)
## 중복데이터 제거
print("중복 제거전 사진수:", len(img_list))
img_list = set(img_list)  # 중복 제거
print('중복 제거후 사진수', len(img_list))
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