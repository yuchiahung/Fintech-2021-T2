### ----- Sentiment Analysis ----- ###
import pandas as pd
import re
df = pd.read_json('../streamlit_summary_web/data/data_summary.json')
df.drop_duplicates(subset=['header', 'source', 'time', 'content', 'link'], inplace = True)

# if there's old sentiment data
try:
    old_sentiment = pd.read_json('../streamlit_summary_web/data/data_sentiment.json')
    df_new = df[~df.header.isin(old_sentiment.header)]
except:
    old_sentiment = pd.DataFrame()
    df_new = df.copy()
    print("There's no old sentiment summary.")
df_new.reset_index(inplace = True, drop = True)


# use "Loughran-McDonald Sentiment Word Lists"
import pysentiment2 as ps
lm = ps.LM()
df_new[['compound', 'pos', 'neg', 'sentiment']] = 0
for i, header in enumerate(df_new['header']):
    tokens = lm.tokenize(header)
    score = lm.get_score(tokens)
    df_new.loc[i, 'compound'] = score["Polarity"]
    df_new.loc[i, 'pos'] = score["Positive"]
    df_new.loc[i, 'neg'] = score["Negative"]
    if score["Polarity"] > 0:
        df_new.loc[i, 'sentiment'] = 1 # positive
    elif score["Polarity"] < 0:
        df_new.loc[i, 'sentiment'] = -1 # negative
    else:
        df_new.loc[i, 'sentiment'] = 0 # neutral
all_sentiment = pd.concat([old_sentiment, df_new], axis = 0)
all_sentiment.to_json('../streamlit_summary_web/data/data_sentiment.json', force_ascii=False)

# use nltk: SentimentIntensityAnalyzer
"""
positive sentiment: compound score >= 0.05
neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
negative sentiment: compound score <= -0.05
"""
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
df_new[['compound', 'pos', 'neu', 'neg', 'sentiment']] = 0
# Use "header" only
for i, header in enumerate(df_new['header']):
    compound = analyzer.polarity_scores(header)["compound"]
    df_new.loc[i, 'compound'] = compound
    df_new.loc[i, 'pos'] = analyzer.polarity_scores(header)["pos"]
    df_new.loc[i, 'neu'] = analyzer.polarity_scores(header)["neu"]
    df_new.loc[i, 'neg'] = analyzer.polarity_scores(header)["neg"]
    if compound >= 0.05:
        df_new.loc[i, 'sentiment'] = 1 # positive
    elif compound <= -0.05:
        df_new.loc[i, 'sentiment'] = -1 # negative
    else:
        df_new.loc[i, 'sentiment'] = 0 # neutral
all_sentiment = pd.concat([old_sentiment, df_new], axis = 0)
all_sentiment.to_json('../streamlit_summary_web/data/data_sentiment.json', force_ascii=False)
"""



### ----- NER Model (extract person, location, organization) ----- ###

from mitie import *
from collections import Counter
from itertools import chain, islice
# df = pd.read_json('../streamlit_summary_web/test_sentiment.json')
# Loading NER model
ner = named_entity_extractor('ner_model.dat')
# print("\nTags output by this NER model:", ner.get_possible_ner_tags())

# if there's old NER data
try:
    old_ner = pd.read_json('../streamlit_summary_web/data/data_ner.json')
    df_ner_new = all_sentiment[~all_sentiment.header.isin(old_ner.header)]
except:
    old_ner = pd.DataFrame()
    df_ner_new = all_sentiment.copy()
    print("There's no old NER data.")

df_ner_new[['org', 'person', 'loc', 'misc']] = '0'
df_ner_new.reset_index(drop = True, inplace = True)
# Find top3 entities (by tf) for each tag (threshold: score > 0.1)
for i in range(len(df_ner_new)):
    # Use 'content' only
    tokens = tokenize(df_ner_new.loc[i, 'content'])
    entities = ner.extract_entities(tokens)
    org, person, loc, misc = [], [], [], []
    for e in entities:
        ran, tag, score = e
        if score > 0.1:
            entity_text = ' '.join(tokens[i].decode() for i in ran)
            if tag == 'ORGANIZATION':
                org.append(entity_text)
            elif tag == 'PERSON':
                person.append(entity_text)
            elif tag == 'LOCATION':
                loc.append(entity_text)
            else:
                misc.append(entity_text)
    df_ner_new.at[i, 'org'] = tuple([c[0] for c in Counter(org).most_common(3)])
    df_ner_new.at[i, 'person'] = tuple([c[0] for c in Counter(person).most_common(3)])
    df_ner_new.at[i, 'loc'] = tuple([c[0] for c in Counter(loc).most_common(3)])
    df_ner_new.at[i, 'misc'] = tuple([c[0] for c in Counter(misc).most_common(3)])

all_ner = pd.concat([old_ner, df_ner_new], axis = 0)
all_ner.to_json('../streamlit_summary_web/data/data_ner.json')


###### Below: Do all the data even if they already existed #####
#### only use tags: `org` & `person`
def manipulate_entities(tag = 'org', n = 2, df_sen_ner = all_ner.copy()):
    """ Entities appears more than n news articles"""
    all_e = list(chain.from_iterable(t for t in df_sen_ner[tag].values))
    important = [k for k, v in Counter(all_e).items() if v > n]
    df_explode = df_sen_ner.explode(tag)
    df_s = df_explode.loc[df_explode[tag].isin(important), [tag, 'sentiment', 'id']]
    df_s.columns = ['entities', 'sentiment', 'news_id']
    # df_s['tags'] = tag
    return df_s

entities_sen_news = pd.DataFrame(columns = ['entities', 'sentiment', 'news_id'])
for t in ['org', 'person']:
    entities_sen_news = pd.concat([entities_sen_news, manipulate_entities(tag = t, n = 2, df_sen_ner = all_ner.copy())])
# remove " Inc" (e.g. Tesla Inc --> Tesla)
entities_sen_news['entities'] = [re.sub('\sInc$', '', e) for e in entities_sen_news.entities]
# drop duplicates (in case there's one entity in two tags at the same time)
entities_sen_news.drop_duplicates(ignore_index = True, inplace = True)
entities_sen_news.to_json('../streamlit_summary_web/data/data_entities_news.json', force_ascii=False)


#### calculate positive rate...
entities_pos_rate = entities_sen_news.groupby(by = ['entities', 'sentiment']).count().reset_index().pivot_table(index = 'entities', columns = 'sentiment', values = 'news_id', fill_value = 0).reset_index()
# in case one of sentiment is missing
if -1 not in entities_pos_rate.columns: 
    entities_pos_rate[-1] = 0
if 0 not in entities_pos_rate.columns:
    entities_pos_rate[0] = 0
if 1 not in entities_pos_rate.columns:
    entities_pos_rate[1] = 0
# calculate sensetive rate
entities_pos_rate['sum'] = entities_pos_rate.iloc[:, 1:].sum(axis = 1)
entities_pos_rate['positive_rate'] = entities_pos_rate[1]/entities_pos_rate['sum']
entities_pos_rate['neutral_rate'] = entities_pos_rate[0]/entities_pos_rate['sum']
entities_pos_rate['negative_rate'] = entities_pos_rate[-1]/entities_pos_rate['sum']

entities_pos_rate.to_json('../streamlit_summary_web/data/data_entities_pos_rate.json', force_ascii=False)