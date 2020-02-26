import sys,os 
sys.path.append(os.getcwd())
import requests
from backend import config 
import re 
import time
import json
import pandas as pd
# from lxml import etree
from datetime import datetime 

import datetime
from backend import parseTable 



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

    def save_pages(self, df, filename):
        if not os.path.isfile(filename):
            df.to_csv(filename, index=False)
        else:
            df.to_csv(filename, mode='a', header=False, index=False)    

    def get_onepage(self,page):
        newUrl = config.entry.replace("p=1", "p=" + str(page))
        print(newUrl)
        raw_result = self.handle_request(method='POST', url=newUrl)
        dfs = pd.read_html(raw_result) # Returns list of all tables on page


        # 每次运行之前需要先清空，因为目前没有去重
        # 使用put 只能存100行。 
        # store = pd.HDFStore('ether.h5')
        # store.append('ether', dfs[0], formart='t', data_columns=True, min_itemsize={'Gas Price': 20})
        # store the data to csv 

        # save the original table
        # dfs[0].to_csv('ether_origin.csv',mode='a',index=False)
        self.save_pages(dfs[0], 'ether_origin.csv')

        # Last Seen to Datetime
        dfs[0]['Datetime'] = dfs[0]['Last Seen'].apply(parseTable.string_to_time)
        # Last seen to seconds int
        dfs[0]['Last Seen / secs'] = dfs[0]['Last Seen'].apply(parseTable.string_to_secs)
        # Gas Limit str to float
        # dfs[0]['Gas Limit'] = dfs[0]['Gas Limit'].apply(float)
        # Gas Price str to float
        dfs[0]['Gas Price / Gwei'] = dfs[0]['Gas Price'].apply(parseTable.value)
        # Value str to float
        dfs[0]['Value / Ether'] = dfs[0]['Value'].apply(parseTable.value)
        dfs[0] = dfs[0].drop(columns=['Last Seen','Gas Price','Value'])
        
        # save the modified table
        # dfs[0].to_csv('modiEther.csv',mode='a',index=False)
        self.save_pages(dfs[0], 'modiEther.csv')

        # save the minified table
        # minidf = dfs[0].loc[:,['Gas Price / Gwei','Gas Limit','Last Seen / secs','Value / Ether','Datetime']]
        # minidf.to_csv('miniEther.csv', mode='a', index = False)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.get_page()
    print(crawler.pages)
    # for i in range(crawler.pages):
    for i in range(1,3):
        # time.sleep(0.5)
        time.sleep(1)
        crawler.get_onepage(i)