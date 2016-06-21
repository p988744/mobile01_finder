import json
from pprint import pprint
# articles = open("results/target_list.txt",'r').read()
with open("results/target_list.txt",'r') as data_file:
    data = json.load(data_file)
print data.keys() 