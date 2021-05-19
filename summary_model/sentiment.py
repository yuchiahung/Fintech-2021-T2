
import pandas as pd
### ----- Sentiment Analysis ----- ###

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_json('../streamlit_summary_web/test_data.json')
analyzer = SentimentIntensityAnalyzer()

"""
positive sentiment: compound score >= 0.05
neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
negative sentiment: compound score <= -0.05
"""

# Use "header" only
df[['compound', 'pos', 'neu', 'neg', 'sentiment']] = 0
df.reset_index(inplace = True, drop = True)
for i, header in enumerate(df['header']):
    compound = analyzer.polarity_scores(header)["compound"]
    df.loc[i, 'compound'] = compound
    df.loc[i, 'pos'] = analyzer.polarity_scores(header)["pos"]
    df.loc[i, 'neu'] = analyzer.polarity_scores(header)["neu"]
    df.loc[i, 'neg'] = analyzer.polarity_scores(header)["neg"]
    if compound >= 0.05:
        df.loc[i, 'sentiment'] = 1 # positive
    elif compound <= -0.05:
        df.loc[i, 'sentiment'] = -1 # negative
    else:
        df.loc[i, 'sentiment'] = 0 # neutral

df.to_json('../streamlit_summary_web/test_sentiment.json', force_ascii=False)



### ----- NER Model (extract person, location, organization) ----- ###

from mitie import *
from collections import Counter
from itertools import chain, islice
# df = pd.read_json('../streamlit_summary_web/test_sentiment.json')
# Loading NER model
ner = named_entity_extractor('ner_model.dat')
print("\nTags output by this NER model:", ner.get_possible_ner_tags())

df[['org', 'person', 'loc', 'misc']] = '0'
# Find top3 entities (by tf) for each tag
for i in range(len(df)):
    # Use 'content' only
    tokens = tokenize(df.loc[i, 'content'])
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
    df.at[i, 'org'] = tuple([c[0] for c in Counter(org).most_common(3)])
    df.at[i, 'person'] = tuple([c[0] for c in Counter(person).most_common(3)])
    df.at[i, 'loc'] = tuple([c[0] for c in Counter(loc).most_common(3)])
    df.at[i, 'misc'] = tuple([c[0] for c in Counter(misc).most_common(3)])


def manipulate_entities(tag = 'org', n = 1, df1 = df.copy(), df_sentiment = df_sentiment_all.copy()):
    """ Entities appears more than n news articles"""
    all_e = list(chain.from_iterable(t for t in df[tag].values))
    important = [k for k, v in Counter(all_e).items() if v > n]
    df_explode = df1.explode(tag)
    df_s = df_explode.loc[df_explode[tag].isin(important), [tag, 'sentiment', 'id']]
    df_s.columns = ['entities', 'sentiment', 'news_id']
    df_s['tags'] = tag
    df_sentiment = pd.concat([df_sentiment, df_s])
    return df_sentiment

df_sentiment_all = pd.DataFrame(columns = ['tags', 'entities', 'sentiment', 'news_id'])
for t in ['org', 'person', 'loc', 'misc']:
    df_sentiment_all = manipulate_entities(tag = t, df_sentiment = df_sentiment_all.copy(), n = 1)

# calculate positive rate...
df_pivot = df_sentiment_all.groupby(by = ['tags', 'entities', 'sentiment']).count().reset_index().pivot_table(index = ['tags', 'entities'], columns = 'sentiment', values = 'news_id', fill_value = 0).reset_index()
if -1 not in df_pivot.columns: 
    df_pivot[-1] = 0
if 0 not in df_pivot.columns:
    df_pivot[0] = 0
if 1 not in df_pivot.columns:
    df_pivot[1] = 0
df_pivot['sum'] = df_pivot.iloc[:, 2:].sum(axis = 1)
df_pivot['positive_rate'] = df_pivot[1]/df_pivot['sum']
df_pivot['neutral_rate'] = df_pivot[0]/df_pivot['sum']
df_pivot['negative_rate'] = df_pivot[-1]/df_pivot['sum']



df_sentiment_all.reset_index(drop=True).to_json('../streamlit_summary_web/test_sentiment_entities.json', force_ascii=False)
df_pivot.to_json('../streamlit_summary_web/test_positive_rate.json', force_ascii=False)


# having person & org only
df_sentiment_all_per_org = df_sentiment_all[df_sentiment_all.tags.isin(['org', 'person'])].drop(columns = 'tags').drop_duplicates()
# having more than 1 letter
df_sentiment_all_per_org = df_sentiment_all_per_org[df_sentiment_all_per_org.entities.str.len() > 1]

df_sentiment_all_per_org.reset_index(drop=True).to_json('../streamlit_summary_web/test_sentiment_entities_person_org.json', force_ascii=False)

df_pivot_limit = df_sentiment_all_per_org.groupby(by = ['entities', 'sentiment']).count().reset_index().pivot_table(index = 'entities', columns = 'sentiment', values = 'news_id', fill_value = 0).reset_index()
if -1 not in df_pivot_limit.columns: 
    df_pivot_limit[-1] = 0
if 0 not in df_pivot_limit.columns:
    df_pivot_limit[0] = 0
if 1 not in df_pivot_limit.columns:
    df_pivot_limit[1] = 0
df_pivot_limit['sum'] = df_pivot_limit.iloc[:, 1:].sum(axis = 1)
df_pivot_limit['positive_rate'] = df_pivot_limit[1]/df_pivot_limit['sum']
df_pivot_limit['neutral_rate'] = df_pivot_limit[0]/df_pivot_limit['sum']
df_pivot_limit['negative_rate'] = df_pivot_limit[-1]/df_pivot_limit['sum']
df_pivot_limit.to_json('../streamlit_summary_web/test_positive_rate_person_org.json', force_ascii=False)