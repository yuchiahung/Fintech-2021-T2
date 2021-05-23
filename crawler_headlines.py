#每日頭條20則
import requests
# from newsapi.newsapi_client import NewsApiClient
from newsapi import NewsApiClient
import json
import pandas as pd
from GoogleNews import GoogleNews
from goose3 import Goose
from goose3.text import StopWordsChinese 


def headlineCrawler(old_dataDict = dict()):
    """get top headlines in category `business` (at most 100)"""
    dataDict = dict()
    if old_dataDict:
        n = len(old_dataDict['id'])
        idDict = old_dataDict['id']
        headerDict = old_dataDict['header']
        sourceDict = old_dataDict['source']
        timeDict = old_dataDict['time']
        contentDict = old_dataDict['content']
        linkDict = old_dataDict['link']
    else:
        n = 0
        idDict = dict()
        headerDict = dict()
        sourceDict = dict()
        timeDict = dict()
        contentDict = dict()
        linkDict = dict()
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&pageSize=100&language=en&apiKey=0bd726adde3042e2810aec5171b67fcc')
    data = json.loads(r.content)
    for i in range(len(data['articles'])):  # at most 100 news
        g = Goose() # {'stopwords_class': StopWordsChinese} 
        # 文章地址
        url = data['articles'][i]['url']
        # 獲取文章內容 
        article = g.extract(url=url) 
        g = Goose()
        article = g.extract(url=url)
        # article.title
        # article.cleaned_text[:200]
        idDict[n+i] = n+i+1
        headerDict[n+i] = data['articles'][i]['title']
        sourceDict[n+i] = data['articles'][i]['source']['name']
        timeDict[n+i] = data['articles'][i]['publishedAt']
        contentDict[n+i] = article.cleaned_text
        linkDict[n+i] = data['articles'][i]['url']
    dataDict["id"] = idDict
    dataDict["header"] = headerDict
    dataDict["source"] = sourceDict
    dataDict["time"] = timeDict
    dataDict["content"] = contentDict
    dataDict["link"] = linkDict
    
    return dataDict

# if already had data file: read file
with open('data_headlines.json', 'r') as fp:
    old_data = json.load(fp)

# add news 
dataDict_headlines = headlineCrawler(old_data)

# save as json file 
with open('data_headlines.json', 'w') as fp:
    json.dump(dataDict_headlines, fp)