# encoding: utf-8
import random
import time
import requests
import urllib
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
from selenium import webdriver
import selenium.webdriver.support.ui as ui


target = "http://img.chinamaxx.net/n/abroad/hwbook/chinamaxx/11293662/cdd340c41f144bf7bb7ee5280542de27/b1976215a542250894a682a98378dd50.shtml?tp=jpabroad&fenlei=&pdgURL=book%3A%2F%2Fread.chinamaxx.net%3A8080%2Fss2path%2Fss2path.dll%3Fssid%3D11293662%26a%3D87B5010D30E32684BA4014D3FF490EA36A6A6B726C6F6F6B3935343238353139%26bed%3D2016-06-23%26ua%3DCBD932C99F0E725FAE29246EE9B36E24ff56b2c1f1794b98affd3bed6bcc1b8f%26dun%3DNTUreader%26pagenum%3D1%26pagetype%3D6&t=1&username=NTUreader"
ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
driver = webdriver.Firefox()  # Optional argument, if not specified will search path.

driver.get("%s"%(target));
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
wait = ui.WebDriverWait(driver,10)

soup = BeautifulSoup(driver.page_source.replace("&lt;","<").replace("&gt;",">"), "lxml")

total_pages = int(soup.select("#Bar h5")[0].get_text().split(" ")[1].split(":")[-1])
print total_pages
total_pages = 20

for page in range(1,total_pages):
	driver.find_element_by_css_selector("#nextPage").click()
	wait = ui.WebDriverWait(driver,10)
	soup = BeautifulSoup(driver.page_source.replace("&lt;","<").replace("&gt;",">"), "lxml")
	print soup.select(".readerImg")[page].get("src") 
	base_url = "http://img.chinamaxx.net"+soup.select(".readerImg")[page].get("src") 
	path_name = "images_fetcher/"
	file_name = str(page)
	urllib.request.urlretrieve(base_url, path_name + file_name)

# soup = BeautifulSoup(driver.page_source.replace("&lt;","<").replace("&gt;",">"), "lxml")
count = 0
for entry in soup.select(".readerImg"):
	if entry.get("src") != "/images/dot.gif":
		print entry.get("src") 
		count=count+1
print count
driver.quit()

