# encoding: utf-8
import random
import time
import requests
import MySQLdb
import re
import io
import os
import sys
import db_settings
import functions
from bs4 import BeautifulSoup
import lxml
from colorama import init
from colorama import Fore, Back, Style
import time
import  json
from operator import itemgetter, attrgetter

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 20):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        print("\n")

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def get_article_comment(host_url,url):
	res = rs.get(host_url+url, headers=ua)
	soup = BeautifulSoup(res.text, "lxml")
	comment_pages = soup.select(".contentfoot .numbers")[0].get_text().encode("utf-8")
	print "total comment pages: "+comment_pages.split('(共')[-1].replace('頁)','')
	comments = soup.select('main .single-post')
	comment_data_dict = {}
	for comment in comments:
		comment_author = comment.select(".single-post-author .fn")[0].get_text().encode("utf-8")
		comment_id = comment.select('.single-post-content div')[0].get('id').encode("utf-8")
		comment_create_time = comment.select(".single-post-author .date")[0].get_text().encode("utf-8").split('#')[0]
		comment_number = comment.select(".single-post-author .date")[0].get_text().encode("utf-8").split('#')[1]
		comment_content = comment.select(".single-post-content")[0].get_text().encode("utf-8")
		comment_data = {
			"author" : comment.select(".single-post-author .fn")[0].get_text().encode("utf-8"),
			"id" : comment.select('.single-post-content div')[0].get('id').encode("utf-8"),
			"create_time" : comment.select(".single-post-author .date")[0].get_text().encode("utf-8").split('#')[0],
			"number" : comment.select(".single-post-author .date")[0].get_text().encode("utf-8").split('#')[1],
			"content" : comment.select(".single-post-content")[0].get_text().encode("utf-8")
		}
		print "---------- Comment: %s ----------"%(comment_number)
		print ">>id: %s\n>>回應者: %s\n>>回應順序: %s\n>>回應時間: %s\n>>回應內容: %s\n"%(comment_data["id"],comment_data["author"],comment_data["number"],comment_data["create_time"],comment_data["content"])
		# break
		comment_data_dict = merge_two_dicts(comment_data_dict,{ comment_id : comment_data })
	return comment_data_dict

def get_board_content(host_url,url):
	res = rs.get(host_url+url, headers=ua)
	soup = BeautifulSoup(res.text, "lxml")
	article_entrys=soup.select('#maincontent')

	if len(article_entrys) == 1:
		article_entry=article_entrys[0]
	##### 取得文章列表 #####
	articles = article_entry.select('.tablelist tbody tr')
	# articles = articles.select('tbody')
	page_article_list = []
	article_data_dict = {}
	for article in articles:
		article_title = article.select('.subject a')[0].get_text().encode("utf-8") # 主題
		article_url = article.select('.subject a')[0].get('href') #文章網址
		article_popularity = article.select('.subject a')[0].get('title').encode("utf-8").replace('人氣:','') # 人氣
		article_reply_amount = article.select('.reply')[0].get_text().encode("utf-8").replace(",",'')  # 回覆數量
		article_time = article.select('.authur a p')[0].get_text().encode("utf-8") # 新增時間
		article_author = article.select('.authur a')[0].get_text().encode("utf-8").replace(article_time,'') # 作者
		article_comment_pages = int(article_reply_amount)/10+1 if (int(article_reply_amount)%10 != 0) | (int(article_reply_amount)%10 == 0) else int(article_reply_amount)/10
		article_data = {
			"title" : article_title, # 主題
			"url" : article_url, #文章網址
			"popularity" : article_popularity, # 人氣
			"reply_amount" : article_reply_amount,  # 回覆數量
			"time" : article_time, # 新增時間
			"author" : article_author, # 作者
			"comment_pages" : article_comment_pages # 回應總頁數
		}
		# print article_data
		article_data_dict = merge_two_dicts(article_data_dict,{ article_url : article_data })
		
		
		page_article_list.append([str(board_title),str(article_title),str(article_author),str(article_reply_amount),str(article_time),str(article_popularity),str(article_url)])
		comment_pages = int(article_reply_amount)/10+1 if int(article_reply_amount)%10 != 0 else int(article_reply_amount)/10
		# print comment_pages
		for comment_page in range(1,comment_pages+1):
			# time.sleep(float(random.randint(100,300))/100) 
			commemt_url = article_url + "&p=" + str(comment_page)
			# print commemt_url
			# get_article_comment(host_url,article_url,comment_page)
	# print article_data_dict.keys()
	return article_data_dict

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
	##### 取得所有文章網址 #####
	articles = {} 
	for page in range(1,pages+1):
		page_url = url+"&p="+str(page)
		articles = merge_two_dicts(articles,get_board_content(host_url,page_url))
		time.sleep(float(random.randint(100,200))/100) # 版面走訪太快會被ban
		printProgress (page, pages, prefix = 'fetching Links...', suffix = '', decimals = 2, barLength = 20)
		break

	for key in articles.keys():

		article_id = articles[key]["url"].split('&t=')[-1]
		articles[key].update({"id":article_id})
		print "================= Article: %s ================="%(article_id)
		print ">主題編號: %s\n>主題: %s\n>作者: %s\n>回覆數量: %s\n>回覆頁數: %s\n>新增時間: %s\n>人氣:% s\n>文章網址: % s"%(str(articles[key]["id"]),str(articles[key]["title"]),str(articles[key]["author"]),str(articles[key]["reply_amount"]),str(articles[key]["comment_pages"]),str(articles[key]["time"]),str(articles[key]["popularity"]),str(articles[key]["url"]))
		print "===============================================" + '='*(len(article_id)-1)

		comments = {}
		for comment_page in range(1,int(articles[key]["comment_pages"])):
			comment_page_url = articles[key]["url"]+"&p="+str(comment_page)
			comments = merge_two_dicts(comments,get_article_comment(host_url,comment_page_url))
			time.sleep(float(random.randint(100,200))/100) # 版面走訪太快會被ban
			printProgress (articles.keys().index(key), len(articles.keys()), prefix = 'fetching articles...', suffix = '', decimals = 2, barLength = 20)
			# break
		articles[key].update({"comments":comments})
		# time.sleep(float(random.randint(100,200))/100) # 版面走訪太快會被ban

data = json.dumps(articles, ensure_ascii=False)
print "++++++++++++++++++++++++++ JSON ++++++++++++++++++++++++++"
print data

# 檢查目錄是否存在
directory = "results"
if not os.path.exists(directory):
    os.makedirs(directory)
with open('results/data.txt', 'w') as outfile:
    json.dump(unicode(data, "utf-8"), outfile)

