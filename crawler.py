import requests
from newsapi.newsapi_client import NewsApiClient
import json
import pandas as pd
from GoogleNews import GoogleNews
from goose3 import Goose
from goose3.text import StopWordsChinese 

#獲的每日商業新聞頭版20則
r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=0bd726adde3042e2810aec5171b67fcc')
data = json.loads(r.content)
print(data)
pdlist = []
dataDict = dict()
idDict = dict()
headerDict = dict()
sourceDict = dict()
contentDict = dict()
linkDict = dict()
for i in range(20):
    print(data['articles'][i]['url'])
    #pdlist[i] = data['articles'][i]['url']
    #print(pdlist[i])
    g = Goose({'stopwords_class': StopWordsChinese}) 
    # 文章地址
    url = data['articles'][i]['url']
    # 獲取文章內容 
    article = g.extract(url=url) 
    # 標題 
    #print(i)
    #print('標題：', article.title) 
    # 顯示正文 
    #print("內文")
    #print(article.cleaned_text)
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




#獲得該主題的容
import requests
from newsapi import NewsApiClient
import json
import pandas as pd
from GoogleNews import GoogleNews
from goose3 import Goose
from goose3.text import StopWordsChinese 
point = 'taiwan'
my_api = '0bd726adde3042e2810aec5171b67fcc'
time = '2021-04-19'

r = requests.get('https://newsapi.org/v2/everything?q='+point+'&from='+time+'+&pageSize=100&sortBy=publishedAt&apiKey='+my_api)

data = json.loads(r.content)
print
print(data)
pdlist = []
dataDict = dict()
idDict = dict()
headerDict = dict()
sourceDict = dict()
contentDict = dict()
linkDict = dict()
print( data['totalResults'])
for i in range(100):
    print(data['articles'][i]['url'])
    #pdlist[i] = data['articles'][i]['url']
    #print(pdlist[i])
    g = Goose({'stopwords_class': StopWordsChinese}) 
    # 文章地址
    url = data['articles'][i]['url']
    # 獲取文章內容 
    article = g.extract(url=url) 
    # 標題 
    #print(i)
    #print('標題：', article.title) 
    # 顯示正文 
    #print("內文")
    #print(article.cleaned_text)
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
