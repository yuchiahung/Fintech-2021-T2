
#獲得該主題的內容 (by keyword)
import requests
# from newsapi.newsapi_client import NewsApiClient
# from newsapi import NewsApiClient
import json
import pandas as pd
import re
# from GoogleNews import GoogleNews
from goose3 import Goose
# from goose3.text import StopWordsChinese 
import datetime
from dateutil.relativedelta import relativedelta
sp500 = pd.read_csv('data/constituents_csv.csv')
sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]
sp500.loc[:, 'name_full'] = ['+'.join(n.split(' ')) for n in sp500.Name]

a_month_ago = (datetime.datetime.now().date() - relativedelta(months=1)).strftime('%Y-%m-%d')

def topicCrawler(point = 'Adobe', idname = 'ADBE', from_time = a_month_ago):
    """ get news by keyword (at most 100 news)"""
    api2 = '6d303029151845f8925f24908a6ff268'
    api3 = '2fe4a31f23ce40d694fe7136c75d23fb'
    api4 = 'e65f4dce1f574854ba4fe0241cb75b46'
    api5 = '67f14d94b2b6487e9d625b93de96fffc'
    # api1 = '0bd726adde3042e2810aec5171b67fcc'
    r = requests.get('https://newsapi.org/v2/everything?q='+point+'&from='+from_time+'+&pageSize=100&sortBy=relevancy&language=en&apiKey='+api5)
    data = json.loads(r.content)
    dataDict = dict()
    idDict = dict()
    headerDict = dict()
    sourceDict = dict()
    timeDict = dict()
    contentDict = dict()
    linkDict = dict()
    for i in range(len(data['articles'])):
        # print(i)
        try:
            g = Goose() # {'stopwords_class': StopWordsChinese}
            # 文章地址
            url = data['articles'][i]['url']
            # 獲取文章內容 
            article = g.extract(url=url)
            # article.title
            # article.cleaned_text[:200]
            idDict[i] = idname + '_' + str(i+1).zfill(4)
            headerDict[i] = data['articles'][i]['title']
            sourceDict[i] = data['articles'][i]['source']['name']
            timeDict[i] = data['articles'][i]['publishedAt']
            contentDict[i] = article.cleaned_text
            linkDict[i] = data['articles'][i]['url']
        except:
            print(f'cannot extract {i}th article')
    dataDict["id"] = idDict
    dataDict["header"] = headerDict
    dataDict["source"] = sourceDict
    dataDict["time"] = timeDict
    dataDict["content"] = contentDict
    dataDict["link"] = linkDict
    return dataDict


# keyword = 'Apple'
# from_date = '2021-05-01'
# dataDict = topicCrawler(point = keyword, from_time = from_date)


# df_all = pd.DataFrame()
df_all = pd.read_json('data/data_sp500.json')

for j in range(len(sp500)):
# for j in range(415, 420):
    print(f'{j}th company...')
    name_clean, symbol = sp500.loc[j, ['name_clean', 'Symbol']]
    df = pd.DataFrame(topicCrawler(point = name_clean, idname = symbol, from_time = a_month_ago))
    df['company'] = name_clean
    df_all = pd.concat([df_all, df], ignore_index=True)
    df_all.to_json('data/data_sp500.json', force_ascii=False)


# # save as json file 
# with open('data/data_{}_{}.json'.format(keyword, from_date), 'w') as fp:
#     json.dump(dataDict, fp)