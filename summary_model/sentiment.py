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
# use nltk: SentimentIntensityAnalyzer
"""
positive sentiment: compound score >= 0.05
neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
negative sentiment: compound score <= -0.05
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
df_new.loc[:, ['compound', 'pos', 'neg', 'sentiment', 'nltk_compound', 'nltk_pos', 'nltk_neu', 'nltk_neg', 'nltk_sentiment']] = 0

# Use "header" only
for i, header in enumerate(df_new['header']):
    # LM dictionary: 超過七成是中立
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
    # NLTK: 快五成中立（正面多於負面）
    compound = analyzer.polarity_scores(header)["compound"]
    df_new.loc[i, 'nltk_compound'] = compound
    df_new.loc[i, 'nltk_pos'] = analyzer.polarity_scores(header)["pos"]
    df_new.loc[i, 'nltk_neu'] = analyzer.polarity_scores(header)["neu"]
    df_new.loc[i, 'nltk_neg'] = analyzer.polarity_scores(header)["neg"]
    if compound >= 0.05:
        df_new.loc[i, 'nltk_sentiment'] = 1 # positive
    elif compound <= -0.05:
        df_new.loc[i, 'nltk_sentiment'] = -1 # negative
    else:
        df_new.loc[i, 'nltk_sentiment'] = 0 # neutral
    # combine two sentiment
    if df_new.loc[i, 'sentiment'] == 0:
        df_new.loc[i, 'final_sentiment'] = df_new.loc[i, 'nltk_sentiment']
    else:
        df_new.loc[i, 'final_sentiment'] = df_new.loc[i, 'sentiment']    

all_sentiment = pd.concat([old_sentiment, df_new], axis = 0)
all_sentiment.reset_index(drop=True, inplace=True)
all_sentiment.to_json('../streamlit_summary_web/data/data_sentiment.json', force_ascii=False)


### ----- NER Model (extract person, location, organization) ----- ###

from mitie import *
from collections import Counter
from itertools import chain, islice, compress
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

df_ner_new.loc[:, ['org', 'person', 'loc', 'misc']] = '0'
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

# read S&P500 company list
sp500 = pd.read_csv('../streamlit_summary_web/data/constituents_csv.csv')
sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]
company_list = sp500.Symbol.tolist() + sp500.Name.tolist() + sp500.name_clean.tolist()

df_ner_new['ner_all'] = df_ner_new[['org', 'person']].values.tolist()
df_ner_new['ner_all'] = [list(chain.from_iterable(n)) for n in df_ner_new.ner_all]
df_ner_new['company_all'] = [list(compress(ner_list, [c in company_list for c in ner_list])) for ner_list in df_ner_new.ner_all]
df_ner_new['company_len'] = [len(c) for c in df_ner_new.company_all]

all_ner = pd.concat([old_ner, df_ner_new], axis = 0)
all_ner.reset_index(drop = True, inplace = True)
all_ner.to_json('../streamlit_summary_web/data/data_ner.json')




###### Below: Do all the data even if they already existed #####
#### only use tags: `org` & `person`
#### only use companies' names
def manipulate_entities(tag = 'org', n = 2, df_sen_ner = all_ner.copy()):
    """ Entities appears more than n news articles"""
    all_e = list(chain.from_iterable(t for t in df_sen_ner[tag].values))
    important = [k for k, v in Counter(all_e).items() if v > n]
    df_explode = df_sen_ner.explode(tag)
    df_s = df_explode.loc[df_explode[tag].isin(important), [tag, 'final_sentiment', 'id']]
    df_s.columns = ['entities', 'sentiment', 'news_id']
    # df_s['tags'] = tag
    return df_s

# entities_sen_news = pd.DataFrame(columns = ['entities', 'final_sentiment', 'news_id'])
# for t in ['org', 'person']:
#     entities_sen_news = pd.concat([entities_sen_news, manipulate_entities(tag = t, n = 2, df_sen_ner = all_ner.copy())])
# remove " Inc" (e.g. Tesla Inc --> Tesla)
# entities_sen_news['entities'] = [re.sub('\sInc$', '', e) for e in entities_sen_news.entities]

entities_sen_news = manipulate_entities(tag = 'company_all', n = 2, df_sen_ner = all_ner.copy())
# replace symbol of companies with their names
for i in range(len(entities_sen_news)):
    if entities_sen_news.loc[i, 'entities'] in sp500.Symbol.tolist():
        entities_sen_news.loc[i, 'entities'] = sp500.loc[sp500.Symbol == entities_sen_news.loc[i, 'entities'], 'name_clean'].values[0]

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