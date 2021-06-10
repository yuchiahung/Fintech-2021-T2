import json
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
ner = en_core_web_sm.load()
from nltk import FreqDist
freq = nltk.FreqDist
import stanza
#stanza.download('en')
from _lzma import *
from _lzma import _encode_filter_properties, _decode_filter_properties
from app_ES import *

#read data
df_environment = pd.read_json('environment5.json')
df_society = pd.read_json('society.json')

#ntlk
def calculate_score(dataframe):
    import pysentiment2 as ps
    lm = ps.LM()
    # use nltk: SentimentIntensityAnalyzer
    """
    positive sentiment: compound score >= 0.05
    neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
    negative sentiment: compound score <= -0.05
    """
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    dataframe.loc[:, ['compound', 'pos', 'neg', 'sentiment', 'nltk_compound', 'nltk_pos', 'nltk_neu', 'nltk_neg', 'nltk_sentiment']] = 0

    # Use "head" only
    for i, row in dataframe.iterrows():
        head = str(dataframe.loc[i, 'head'])
        # LM dictionary: 超過七成是中立
        tokens = lm.tokenize(head)
        score = lm.get_score(tokens)
        dataframe.loc[i, 'compound'] = score["Polarity"]
        dataframe.loc[i, 'pos'] = score["Positive"]
        dataframe.loc[i, 'neg'] = score["Negative"]
        if score["Polarity"] > 0:
            dataframe.loc[i, 'sentiment'] = 1 # positive
        elif score["Polarity"] < 0:
            dataframe.loc[i, 'sentiment'] = -1 # negative
        else:
            dataframe.loc[i, 'sentiment'] = 0 # neutral
        # NLTK: 快五成中立（正面多於負面）
        compound = analyzer.polarity_scores(head)["compound"]
        dataframe.loc[i, 'nltk_compound'] = compound
        dataframe.loc[i, 'nltk_pos'] = analyzer.polarity_scores(head)["pos"]
        dataframe.loc[i, 'nltk_neu'] = analyzer.polarity_scores(head)["neu"]
        dataframe.loc[i, 'nltk_neg'] = analyzer.polarity_scores(head)["neg"]
        if compound >= 0.05:
            dataframe.loc[i, 'nltk_sentiment'] = 1 # positive
        elif compound <= -0.05:
            dataframe.loc[i, 'nltk_sentiment'] = -1 # negative
        else:
            dataframe.loc[i, 'nltk_sentiment'] = 0 # neutral
        # combine two sentiment
        if dataframe.loc[i, 'sentiment'] == 0:
            dataframe.loc[i, 'final_sentiment'] = dataframe.loc[i, 'nltk_sentiment']
        else:
            dataframe.loc[i, 'final_sentiment'] = dataframe.loc[i, 'sentiment'] 
    return dataframe  



def look_company(dataframe):
    collect = []
    #sent_collect = []
    nlp2 = stanza.Pipeline(lang='en', processors='tokenize,ner',use_gpu=True)
    for i, row in dataframe.iterrows():
        sent_ner = nlp2(str(row['head']))
        for ent in sent_ner.ents:
            if (ent.type == 'ORG'):
                collect.append(ent.text)
    top_5 = nltk.FreqDist(collect)
    #print(all_pdf.most_common(5))
    return top_5.most_common(5)
    #return collect
    



    































