#!/usr/bin/python
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
import sys, getopt

def main(argv):
   retry_status = ''
   exist_data_path = ''
   try:
      opts, args = getopt.getopt(argv,"hr:d:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -r <retry> -d <exist data path>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -r <retry> -d <exist data path>'
         sys.exit()
      elif opt in ("-r", "--ifile"):
         retry_status = 1
   print 'retry_status is "', retry_status

if __name__ == "__main__":
   main(sys.argv[1:])