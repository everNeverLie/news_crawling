# -*- coding: utf-8 -*-
import string
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib

def get_article_info(crawl_url, inform_list): # 헤드라인 뉴스 정보 수집 및 추가
    
    temp_result = [] #가져온 기사 정보 리스트 임시 저장
    head_line_list = [] #헤드라인 뉴스 리스트
    related_news_list = [] #관련 뉴스 더보기 링크 저장 
    more_btn = None #헤드라인 뉴스 더보기 버튼 
    
    driver= webdriver.Chrome()
    driver.get(crawl_url)
    page_html = driver.page_source
    url_soup = BeautifulSoup(page_html, 'lxml', from_encoding='utf-8')
    
    more_btn = url_soup.select_one("#main_content > div > div._persist > div.cluster._news_cluster_more_layer > div > a")
    
    #more_btn 찾기
    #more_btn 클릭
    driver.find_element_by_css_selector("#main_content > div > div._persist > div.cluster._news_cluster_more_layer > div > a").click()
    
    if more_btn is not None:
        #head_line_list 찾기 #main_content > div > div._persist > div:nth-child(1) > div:nth-child(1) > div.cluster_foot > div > a
        #//*[@id="main_content"]/div/div[2]/div[1]/div[1]/div[2]/div/a
        head_line_list = url_soup.select("#main_content > div > div._persist > div > div > div.cluster_foot > div > a")
        
        for news in head_line_list:
            more_url = None #관련 뉴스 더보기 버튼에 있는 링크
            
            #more_url 찾기
            more_url = news.get('href')
            
            if more_url is not None:
                related_news_list.append("https://news.naver.com/"+more_url)
            
            else: 
                print("ERROR: 관련 뉴스 더보기 버튼을 찾을 수 없습니다.")
        
        for news_url in related_news_list:
            temp_result = []
            
            temp_result = get_detail_info(news_url, crawl_url[-1])
            
            if len(temp_result)>0:
                
                inform_list.append(temp_result)
                
            else:
                print("ERROR : 관련 뉴스 정보를 찾을 수 없습니다." + "url:" + news_url)
    else:
        print("ERROR : 헤드라인 뉴스 더보기 버튼을 찾을 수 없습니다.")
        
    driver.close()
    print("get_article_info done")

def get_detail_info(news_url, cat_num): # 뉴스 상세정보 수집
    
    news_list = [] #뉴스 리스트 
    result_list = []
    
    driver2= webdriver.Chrome()
    driver2.get(news_url)
    page_html = driver2.page_source
    url_soup = BeautifulSoup(page_html, 'lxml', from_encoding='utf-8')
    
    #news_list 찾기 #main_content > div:nth-child(2) > ul > li
    news_list = url_soup.select("#main_content > div:nth-child(2) > ul > li")
    
    for news in news_list:
        temp_dict = {}
        
        #temp_dict 에 정보 저장
        #텍스트 뽑아낼때 인코딩 문제 해결 필요
        temp_dict["title"] = news.select_one("dl > dt > a").text.encode('utf-8')
        temp_dict["url"] = news.select_one("dl > dt > a").get('href')
        temp_dict["writing"] = news.select_one("span.writing").text.encode('utf-8')
        temp_dict["date"] = news.select_one("span.date").text.encode('utf-8')
        
        #sid1 넘겨 받아야할 필요가 있음
        if cat_num == "0":
            temp_dict["category"] = "정치"
            
        elif cat_num == "1":
            temp_dict["category"] = "경제"
            
        elif cat_num == "2":
            temp_dict["category"] = "사회 "
            
        elif cat_num == "3":
            temp_dict["category"] = "생활/문화 "
            
        elif cat_num == "4":
            temp_dict["category"] = "IT/과학"
            
        elif cat_num == "5":
            temp_dict["category"] = "세계"
        
        # print("temp_dict", temp_dict)    
        result_list.append(temp_dict)
    
    driver2.close()
    print(result_list)
    print("get_detail_info done"+"news_url:"+ news_url)
    return result_list

def main():
    print("main")
    inform_list = [] #추가할 기사 정보 리스트
    start_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10"
    crawl_url=""
    sid1 = ""
    
    for i in range(6):
        sid1 = str(i)
        print(sid1)
        crawl_url = start_url + sid1
        
        print(crawl_url)
        
        get_article_info(crawl_url, inform_list)
        
    #엑셀에 저장
    # df = pd.DataFrame(inform_list)
    
    # file_name = "news_crawling_infrom.xlsx"
    # df.to_excel(file_name)
    
    print("main done")
    
    #print(df)
    
    
if __name__ == "__main__":
            main()   