#每日頭條20則
import requests
from newsapi import NewsApiClient
import json
import pandas as pd
from GoogleNews import GoogleNews
from goose3 import Goose
from goose3.text import StopWordsChinese 
dataDict = dict()
def headlineCrawler(dataDict):
    headerDict = dict()
    sourceDict = dict()
    contentDict = dict()
    linkDict = dict()
    dataDict["id"] = idDict
    dataDict["head"] = headerDict
    dataDict["source"] = sourceDict
    dataDict["content"] = contentDict
    dataDict["link"] = linkDict
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=0bd726adde3042e2810aec5171b67fcc')
    data = json.loads(r.content)
    for i in range(20):
        g = Goose({'stopwords_class': StopWordsChinese}) 
        # 文章地址
        url = data['articles'][i]['url']
        # 獲取文章內容 
        article = g.extract(url=url) 
        g = Goose()
        article = g.extract(url=url)
        article.title
        article.cleaned_text[:200]
        idDict[i] = i+1
        headerDict[i] = data['articles'][i]['title']
        sourceDict[i] = data['articles'][i]['source']['name']
        contentDict[i] = article.cleaned_text[:300]
        linkDict[i] = data['articles'][i]['url']

dataDict = dict()
headlineCrawler(dataDict)

#獲得該主題的容
import requests
from newsapi import NewsApiClient
import json
import pandas as pd
from GoogleNews import GoogleNews
from goose3 import Goose
from goose3.text import StopWordsChinese 


def topicCrawler(point,from_time,dataDict):
    r = requests.get('https://newsapi.org/v2/everything?q='+point+'&from='+time+'+&pageSize=100&sortBy=publishedAt&apiKey=0bd726adde3042e2810aec5171b67fcc')
    data = json.loads(r.content)
    idDict = dict()
    headerDict = dict()
    sourceDict = dict()
    contentDict = dict()
    linkDict = dict()
    for i in range(100):
        g = Goose({'stopwords_class': StopWordsChinese}) 
        # 文章地址
        url = data['articles'][i]['url']
        # 獲取文章內容 
        article = g.extract(url=url) 
        g = Goose()
        article = g.extract(url=url)
        article.title
        article.cleaned_text[:200]
        idDict[i] = i+1
        headerDict[i] = data['articles'][i]['title']
        sourceDict[i] = data['articles'][i]['source']['name']
        contentDict[i] = article.cleaned_text[:300]
        linkDict[i] = data['articles'][i]['url']
    dataDict["id"] = idDict
    dataDict["head"] = headerDict
    dataDict["source"] = sourceDict
    dataDict["content"] = contentDict
    dataDict["link"] = linkDict

point = 'taiwan'
frotime = '2021-04-19'
dataDict = dict()
topicCrawler(point,from_time,dataDict)
