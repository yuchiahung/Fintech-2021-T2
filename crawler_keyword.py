
#獲得該主題的內容 (by keyword)
import requests
# from newsapi.newsapi_client import NewsApiClient
from newsapi import NewsApiClient
import json
import pandas as pd
from GoogleNews import GoogleNews
from goose3 import Goose
from goose3.text import StopWordsChinese 
import datetime
from dateutil.relativedelta import relativedelta


a_month_ago = (datetime.datetime.now().date() - relativedelta(months=1)).strftime('%Y-%m-%d')

def topicCrawler(point = 'Apple', from_time = a_month_ago):
    """ get news by keyword (at most 100 news)"""
    r = requests.get('https://newsapi.org/v2/everything?q='+point+'&from='+from_time+'+&pageSize=100&sortBy=popularity&language=en&apiKey=0bd726adde3042e2810aec5171b67fcc')
    data = json.loads(r.content)
    dataDict = dict()
    idDict = dict()
    headerDict = dict()
    sourceDict = dict()
    timeDict = dict()
    contentDict = dict()
    linkDict = dict()
    for i in range(100):
        g = Goose() # {'stopwords_class': StopWordsChinese}
        # 文章地址
        url = data['articles'][i]['url']
        # 獲取文章內容 
        article = g.extract(url=url)
        # article.title
        # article.cleaned_text[:200]
        idDict[i] = i+1
        headerDict[i] = data['articles'][i]['title']
        sourceDict[i] = data['articles'][i]['source']['name']
        timeDict[i] = data['articles'][i]['publishedAt']
        contentDict[i] = article.cleaned_text
        linkDict[i] = data['articles'][i]['url']
    dataDict["id"] = idDict
    dataDict["head"] = headerDict
    dataDict["source"] = sourceDict
    dataDict["time"] = timeDict
    dataDict["content"] = contentDict
    dataDict["link"] = linkDict
    return dataDict


keyword = 'Apple'
from_date = '2021-05-01'
dataDict = topicCrawler(point = keyword, from_time = from_date)

# save as json file
with open('data/data_{}_{}.json'.format(keyword, from_date), 'w') as fp:
    json.dump(dataDict, fp)
