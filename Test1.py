import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# 로딩시간 대기용
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

query = input("검색어를 입력하세요.")

# 만약 접속이 안 될 경우를 대비 헤더 설정, Headless Chrome 설정
options = webdriver.ChromeOptions()
options.headless = True                         # Headless Chrome
options.add_argument("window-size=1920x1080")   # 창 크기 설정
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")

browser = webdriver.Chrome("C:/PythonScraping/chromedriver.exe", options=options)  # chromedriver로 웹 브라우저 객체 생성
url = "https://arxiv.org/"
browser.get(url)    # 브라우저에서 URL로 이동

search = browser.find_element_by_xpath("//*[@id='header']/div[2]/form/div/div[1]/input").clear()
search = browser.find_element_by_xpath("//*[@id='header']/div[2]/form/div/div[1]/input").send_keys(query)
browser.find_element_by_xpath("//*[@id='header']/div[2]/form/div/div[1]/input").send_keys(Keys.ENTER)

try:
    elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-container']/div[1]")))

    soup = BeautifulSoup(browser.page_source, "lxml")
    results = soup.find_all("li", attrs={"class":"arxiv-result"})   # 검색결과 list로 저장

    for result in results:
        title = result.find("p", attrs={"class":"title is-5 mathjax"}).get_text().strip()   # 제목 텍스트 공백 제거
        link = result.find("p", attrs={"class":"list-title is-inline-block"}).find("a")["href"]   # p하위 첫 번째 a태그의 href

        # pdf, ps, other
        pdf = result.find("p", attrs={"class": "list-title is-inline-block"}).find("span").find_all("a")[0]["href"]
        link_cnt = result.find("p", attrs={"class": "list-title is-inline-block"}).find("span").get_text().count(",")
        if link_cnt == 1:
            other = result.find("p", attrs={"class": "list-title is-inline-block"}).find("span").find_all("a")[1][
                "href"]
        elif link_cnt > 1:
            ps = result.find("p", attrs={"class": "list-title is-inline-block"}).find("span").find_all("a")[1]["href"]
            other = result.find("p", attrs={"class": "list-title is-inline-block"}).find("span").find_all("a")[2][
                "href"]

        aut_cnt = len(result.find("p", attrs={"class":"authors"}).find_all("a"))
        for i in range(0, aut_cnt):
            authors = result.find("p", attrs={"class":"authors"}).find_all("a")[i].get_text()
        abstract = result.find()

        print(title, link_cnt, ps, other)

finally:
    browser.close()






