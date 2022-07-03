from asyncio.windows_events import NULL
from lib2to3.pgen2 import driver
import string
from unittest import result
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib

from urllib3 import NullHandler

driver= webdriver.Chrome()
# url="https://google.com"

# driver.get(url)

def get_article_info(driver, crawl_url, crawl_date, inform_list): # 헤드라인 뉴스 정보 수집 및 추가
    
    temp_result = [] #가져온 기사 정보 리스트 임시 저장
    head_line_list = [] #헤드라인 뉴스 리스트
    related_news_list = [] #관련 뉴스 더보기 링크 저장 
    more_btn = NULL #헤드라인 뉴스 더보기 버튼 
    
    #more_btn 찾기
    #more_btn 클릭
    
    if more_btn is not NULL:
        #head_line_list 찾기
        
        for news in head_line_list:
            more_url = NULL #관련 뉴스 더보기 버튼에 있는 링크
            
            #more_url 찾기
            
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
        
    

def get_detail_info(driver, news_url): # 뉴스 상세정보 수집
    
    news_list = [] #뉴스 리스트 
    result_list = []
    
    #news_list 찾기
    
    for news in news_list:
        temp_dict = {}
        
        #temp_dict 에 정보 저장
        temp_dict["title"] = ""
        temp_dict["category"] = ""
        temp_dict["writing"] = ""
        temp_dict["date"] = ""
        
        result_list.append(temp_dict)
        
    return result_list

def main():
    
    inform_list = [] #추가할 기사 정보 리스트
    start_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1="
    crawl_url=""
    crawl_date = ""
    sid1 = ""
    
    #crawl_date 설정
    
    for i in range(100,5):
        sid1 = string(i)
        crawl_url = start_url + sid1
        
        get_article_info(driver, crawl_url, crawl_date, inform_list)
        
    #엑셀에 저장
    
    