import sys,os 
sys.path.append(os.getcwd())
import requests
from backend import config 
import re 
import time
import json
import pandas as pd
from lxml import etree

class Crawler(object):
    def __init__(self):
        self.crawler_session = requests.session()
        self.header = {
            'User-Agent':config.useragent
        }
        self.pages = 0 

        # 定义公用的请求信息
    def handle_request(self, method, url, data=None, info=None):
        if method == 'GET' or method == 'POST':
            response = self.crawler_session.get(
                url=url,
                headers = self.header
            )
        return response.text   

    def get_page(self):
        raw_result = self.handle_request(method='GET',  url=config.entry)
        # print(raw_result)
        # 使用正则表达式拿到列表
        pages_search = re.compile(config.pRegex)
        self.pages = int(pages_search.findall(raw_result)[0])      
        # print(self.pages)  

    def get_onepage(self,page):
        newUrl = config.entry.replace("p=1", "p=" + str(page))
        print(newUrl)
        raw_result = self.handle_request(method='POST', url=newUrl)
        dfs = pd.read_html(raw_result) # Returns list of all tables on page
        # print(len(dfs)) # 1 only one table exists. 
        # print(dfs[0].loc[:3])
        # print(dfs[0].columns)
        # print(dfs[0].ix[0:3,1:5]) # print an area. 
        # dfs[0].to_sql("daily_flights", conn, if_exists="replace")
        store = pd.HDFStore('ether.h5')
        # store['etherDf'] += dfs[0]
        # idx = store.select('etherDf', where="index in dfs[0].index", columns=['index']).index
        # 每次运行之前需要先清空，因为目前没有去重
        store.append('ether', dfs[0], formart='t', data_columns=True, min_itemsize={'Gas Price': 20})
        # 使用put 只能存100行。 
        # store.put('ether', dfs[0], formart='t', data_columns=True, min_itemsize={'Gas Price': 20})

        

if __name__ == "__main__":
    crawler = Crawler()
    crawler.get_page()
    # for i in range(crawler.pages):
    for i in range(1,3):
        time.sleep(0.03)
        crawler.get_onepage(i)