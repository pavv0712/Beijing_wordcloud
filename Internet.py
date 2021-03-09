from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


driver = webdriver.Chrome()
driver.get('https://internet.bjd.com.cn/')
   
SCROLL_PAUSE_SEC = 3

# 스크롤 높이 가져옴
last_height = driver.execute_script('return document.body.scrollHeight')

while True:
    # 끝까지 스크롤 다운
    try:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    except:
        break
    # 3초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        try:
            driver.find_element_by_xpath('/html/body/main/div/div[3]/p').click()
        except:
            break
    last_height = new_height
    time.sleep(3)

content = driver.find_element_by_xpath('//*[@id="home"]/div/div')

divs = content.find_elements_by_xpath('.//div/div')

arti_detail = []

for div in divs:
    #제목 크롤링
    ps = div.find_element_by_xpath('.//p').text
    print(ps)
    
    div.find_element_by_xpath('.//p').click()

    time.sleep(5)
    
    #새로 열린 탭으로 변경
    driver.switch_to.window(driver.window_handles[-1])

    #새로 열린 탭 크롤링
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select('body > main > div.bjd-row > div.bjd-article-main-centent > div.bjd-article-main > div.bjd-article-title')
    contents = soup.select('body > main > div.bjd-row > div.bjd-article-main-centent > div.bjd-article-main > div.bjd-article-centent')
    
    #zip() 은 동일한 개수로 이루어진 자료형을 묶어 주는 역할을 하는 함수

    for item in zip(title, contents):
        arti_detail.append({
            'title' : item[0].text.replace(' ','').replace('《', '').replace('》', '').replace('，', '').replace('。', '').replace('、','').replace('：', '').replace('“','').replace('”','').replace('？','').replace('.', '').replace('；', '').replace('！', '').replace(',(', '').replace(',)', '').replace('?', ''),
            'content' : item[1].text.replace(' ','').replace('《', '').replace('》', '').replace('，', '').replace('。', '').replace('、','').replace('：', '').replace('“','').replace('”','').replace('？','').replace('.', '').replace('；', '').replace('！', '').replace(',(', '').replace(',)', '').replace('?', '')
        })
        
    print(arti_detail)

    #새로 열린 탭 닫고 기존탭으로 돌아가기

    driver.close()
    
    time.sleep(3)

    first_tab = driver.window_handles[0]

    driver.switch_to.window(window_name=first_tab)

print(arti_detail)
data = pd.DataFrame(arti_detail)
data.to_csv('Culture_news.csv')
print('저장완료')

