# encoding: utf-8
import random
import time
import requests
import MySQLdb
import re
import sys
import db_settings
import functions
from bs4 import BeautifulSoup
import lxml
from colorama import init
from colorama import Fore, Back, Style
import time
import  json

def get_article_comment(host_url,url,page_now):
	res = rs.get(host_url+url, headers=ua)
	soup = BeautifulSoup(res.text, "lxml")
	comment_pages = soup.select(".contentfoot .numbers")[0].get_text().encode("utf-8")
	print "total comment pages: "+comment_pages.split('(共')[-1].replace('頁)','')
	comments = soup.select('main .single-post')
	for comment in comments:
		comment_author = comment.select(".single-post-author .fn")[0].get_text().encode("utf-8")
		comment_id = comment.select('.single-post-content div')[0].get('id').encode("utf-8")
		comment_create_time = comment.select(".single-post-author .date")[0].get_text().encode("utf-8").split('#')[0]
		comment_number = comment.select(".single-post-author .date")[0].get_text().encode("utf-8").split('#')[1]
		comment_content = comment.select(".single-post-content")[0].get_text().encode("utf-8")
		print "---------- Comment: %s ----------"%(comment_number) #((comments.index(comment)+1)+((page_now-1)*10))
		print "id: %s\n回應者: %s\n回應時間: %s\n回應內容: %s\n"%(comment_id,comment_author,comment_create_time,comment_content)
		# break

def get_board_content(host_url,url,page):
	res = rs.get(host_url+url, headers=ua)
	soup = BeautifulSoup(res.text, "lxml")
	article_entrys=soup.select('#maincontent')

	if len(article_entrys) == 1:
		article_entry=article_entrys[0]
	##### 取得文章列表 #####
	articles = article_entry.select('.tablelist tbody tr')
	# articles = articles.select('tbody')
	page_article_list = []
	for article in articles:
		article_title = article.select('.subject a')[0].get_text().encode("utf-8") # 主題
		article_url = article.select('.subject a')[0].get('href') #文章網址
		article_popularity = article.select('.subject a')[0].get('title').encode("utf-8").replace('人氣:','') # 人氣
		article_reply_amount = article.select('.reply')[0].get_text().encode("utf-8")  # 回覆數量
		article_time = article.select('.authur a p')[0].get_text().encode("utf-8") # 新增時間
		article_author = article.select('.authur a')[0].get_text().encode("utf-8").replace(article_time,'') # 作者
		
		print "========== Article: %s =============="%((articles.index(article)+1)+((page-1)*30))
		print "版面標題: %s\n主題: %s\n作者: %s\n回覆數量: %s\n新增時間: %s\n人氣:% s\n文章網址: % s\n"%(str(board_title),str(article_title),str(article_author),str(article_reply_amount),str(article_time),str(article_popularity),str(article_url))
		page_article_list.append([str(board_title),str(article_title),str(article_author),str(article_reply_amount),str(article_time),str(article_popularity),str(article_url)])
		# 版面走訪太快會被ban
		time.sleep(float(random.randint(100,200))/100) 
		comment_pages = int(article_reply_amount)/10+1
		# print comment_pages
		for comment_page in range(1,comment_pages+1):
			time.sleep(float(random.randint(100,300))/100) 
			commemt_url = article_url + "&p=" + str(comment_page)
			# print commemt_url
			get_article_comment(host_url,article_url,comment_page)
		print "===================================="
	return page_article_list

############### main ###############
host_url = "http://www.mobile01.com/"
target = "topiclist.php?f=330"
ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
sort_type = "&sort=topictime"
url = target+sort_type

rs = requests.session()
res = rs.get(host_url+url, headers=ua)
soup = BeautifulSoup(res.text, "lxml")
# print soup

board_title=""

page = 0
entrys=soup.select('#maincontent')

if len(entrys) == 1:
	entry=entrys[0]
	##### 取得討論版面標題 #####
	if len(entry.select('h2'))>1:
		if entry.select('h2')[1]!="精選文章":
			board_title = entry.select('h2')[1].get_text() # 版面標題
			board_title = board_title.encode("utf-8")
			print str(board_title)
	##### 取得總頁數 #####
	pages = int(entry.select('.pagination a')[-1].get_text())
	print "total pages:" + str(pages)
	results = []
	for page in range(1,pages):
		page_url = url+"&p="+str(page)
		# results.append(get_board_content(host_url,page_url,page))
		for result in results:
			# print result
			pass
		# break
		

	# timestamp = time.strftime("%Y%m%d_%H_%M_%S", time.localtime()) 		
	# fw = open("results/%s.txt"%(timestamp),'w')
	# fw.write(results)
	# fw.close()

