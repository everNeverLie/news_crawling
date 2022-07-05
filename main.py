from asyncio.windows_events import NULL
from cgitb import text
from http.client import SWITCHING_PROTOCOLS
from lib2to3.pgen2 import driver
import string
from unittest import result
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib
from urllib3 import NullHandler


def get_article_info(crawl_url, inform_list): # 헤드라인 뉴스 정보 수집 및 추가
    
    temp_result = [] #가져온 기사 정보 리스트 임시 저장
    head_line_list = [] #헤드라인 뉴스 리스트
    related_news_list = [] #관련 뉴스 더보기 링크 저장 
    more_btn = NULL #헤드라인 뉴스 더보기 버튼 
    
    driver= webdriver.Chrome()
    driver.get(crawl_url)
    page_html = driver.page_source
    url_soup = BeautifulSoup(page_html, 'lxml')
    
    more_btn = url_soup.select_one("#main_content > div > div._persist > div.cluster._news_cluster_more_layer > div > a")
    
    #more_btn 찾기
    #more_btn 클릭
    driver.find_element_by_css_selector("#main_content > div > div._persist > div.cluster._news_cluster_more_layer > div > a").click()
    
    if more_btn is not NULL:
        #head_line_list 찾기
        head_line_list = url_soup.select("#main_content > div > div._persist > div.cluster_foot > div > a")
        
        for news in head_line_list:
            more_url = NULL #관련 뉴스 더보기 버튼에 있는 링크
            
            #more_url 찾기
            more_url = news.get('href')
            
            if more_url is not NULL:
                related_news_list.append(more_url)
            
            else: 
                print("ERROR: 관련 뉴스 더보기 버튼을 찾을 수 없습니다.")
        
        for news_url in related_news_list:
            temp_result = []
            
            temp_result = get_detail_info(driver, news_url)
            
            if len(temp_result)>0:
                
                inform_list.append(temp_result)
                
            else:
                print("ERROR : 관련 뉴스 정보를 찾을 수 없습니다." + "url:" + news_url)
    else:
        print("ERROR : 헤드라인 뉴스 더보기 버튼을 찾을 수 없습니다.")
        
    driver.close()
    

def get_detail_info(news_url): # 뉴스 상세정보 수집
    
    news_list = [] #뉴스 리스트 
    result_list = []
    
    driver= webdriver.Chrome()
    driver.get(news_url)
    page_html = driver.page_source
    url_soup = BeautifulSoup(page_html, 'lxml')
    
    #news_list 찾기 #main_content > div:nth-child(2) > ul > li
    news_list = url_soup.select("#main_content > div:nth-child(2) > ul > li")
    
    for news in news_list:
        temp_dict = {}
        
        #temp_dict 에 정보 저장
        temp_dict["title"] = news.select_one("dl > dt > a").text
        temp_dict["url"] = news.select_one("dl > dt > a").get('href')
        temp_dict["writing"] = news.select_one("span.writing").text
        temp_dict["date"] = news.select_one("span.date").text
        
        if news_url[-1] == "0":
            temp_dict["category"] = "정치"
            
        elif news_url[-1] == "1":
            temp_dict["category"] = "경제"
            
        elif news_url[-1] == "2":
            temp_dict["category"] = "사회 "
            
        elif news_url[-1] == "3":
            temp_dict["category"] = "생활/문화 "
            
        elif news_url[-1] == "4":
            temp_dict["category"] = "IT/과학"
            
        elif news_url[-1] == "5":
            temp_dict["category"] = "세계"
            
        result_list.append(temp_dict)
    
    driver.close()
    return result_list

def main():
    
    inform_list = [] #추가할 기사 정보 리스트
    start_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1="
    crawl_url=""
    sid1 = ""
    
    for i in range(100,5):
        sid1 = string(i)
        crawl_url = start_url + sid1
        
        get_article_info(crawl_url, inform_list)
        
    #엑셀에 저장
    df = pd.DataFrame(inform_list)
    
    file_name = "news_crawling_infrom.xlsx"
    df.to_excel(file_name)
    
    print("done")
    
    print(df)
    
    