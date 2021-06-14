
### ----- NER Model (extract person, location, organization) ----- ###

from mitie import *
from collections import Counter
from itertools import chain, islice, compress
import pandas as pd
import re
# df = pd.read_json('../test_sentiment.json')
# Loading NER model
ner = named_entity_extractor('ner_model.dat')
# print("\nTags output by this NER model:", ner.get_possible_ner_tags())

# read data
df_environment = pd.read_json('../streamlit_summary_web/df.json')
df_society = pd.read_json('../streamlit_summary_web/df_2.json')
# read S&P500 company list
sp500 = pd.read_csv('../data/constituents_csv.csv')
sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]
company_list = sp500.Symbol.tolist() + sp500.Name.tolist() + sp500.name_clean.tolist()

def ner_model(df, company_list):
    # clean data
    df.dropna(subset=['head'], inplace = True)
    df_ner = df[df['head'] != 0]
    df_ner.loc[:, ['org', 'person', 'loc', 'misc']] = '0'
    df_ner.reset_index(drop = True, inplace = True)
    # Find top3 entities (by tf) for each tag (threshold: score > 0.1)
    for i in range(len(df_ner)):
        # Use 'content' only
        tokens = tokenize(df_ner.loc[i, 'content'])
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
        df_ner.at[i, 'org'] = tuple([c[0] for c in Counter(org).most_common(3)])
        df_ner.at[i, 'person'] = tuple([c[0] for c in Counter(person).most_common(3)])
        df_ner.at[i, 'loc'] = tuple([c[0] for c in Counter(loc).most_common(3)])
        df_ner.at[i, 'misc'] = tuple([c[0] for c in Counter(misc).most_common(3)])

    df_ner['ner_all'] = df_ner[['org', 'person']].values.tolist()
    df_ner['ner_all'] = [list(chain.from_iterable(n)) for n in df_ner.ner_all]
    df_ner['company_all'] = [list(compress(ner_list, [c in company_list for c in ner_list])) for ner_list in df_ner.ner_all]
    df_ner['company_len'] = [len(c) for c in df_ner.company_all]
    return df_ner

df_environment_ner = ner_model(df_environment, company_list)
df_society_ner = ner_model(df_society, company_list)

df_environment_ner = df_environment_ner[df_environment_ner.company_len != 0]
df_society_ner = df_society_ner[df_society_ner.company_len != 0]
df_environment_ner.drop_duplicates(subset = ['head', 'source', 'content'], inplace = True)
df_society_ner.drop_duplicates(subset = ['head', 'source', 'content'], inplace = True)

df_environment_ner.to_json('../streamlit_summary_web/data/df_environment_ner.json')
df_society_ner.to_json('../streamlit_summary_web/data/df_society_ner.json')



###### Below: Do all the data even if they already existed #####
#### only use tags: `org` & `person`
#### only use companies' names
def manipulate_entities(tag = 'org', n = 2, df_sen_ner = df_environment_ner.copy()):
    """ Entities appears more than n news articles"""
    all_e = list(chain.from_iterable(t for t in df_sen_ner[tag].values))
    important = [k for k, v in Counter(all_e).items() if v > n]
    df_explode = df_sen_ner.explode(tag)
    df_s = df_explode.loc[df_explode[tag].isin(important), [tag, 'sentiment', 'id', 'category']]
    df_s.columns = ['entities', 'sentiment', 'news_id', 'category']
    # df_s['tags'] = tag
    return df_s

### Environment
entities_sen_news_envir = manipulate_entities(tag = 'company_all', n = 1, df_sen_ner = df_environment_ner.copy())
entities_sen_news_envir.reset_index(drop = True, inplace = True)
# replace symbol of companies with their names
for i in range(len(entities_sen_news_envir)):
    if entities_sen_news_envir.loc[i, 'entities'] in sp500.Symbol.tolist():
        entities_sen_news_envir.loc[i, 'entities'] = sp500.loc[sp500.Symbol == entities_sen_news_envir.loc[i, 'entities'], 'name_clean'].values[0]
# drop duplicates (in case there's one entity in two tags at the same time)
entities_sen_news_envir.drop_duplicates(ignore_index = True, inplace = True)
entities_sen_news_envir.to_json('../data/entities_sen_news_envir.json', force_ascii=False)
#### calculate positive rate...
entities_pos_rate = entities_sen_news_envir.groupby(by = ['entities', 'category', 'sentiment']).count().reset_index().pivot_table(index = ['entities', 'category'], columns = 'sentiment', values = 'news_id', fill_value = 0).reset_index()
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
entities_pos_rate.rename(columns = {-1:'-1', 0:'0', 1:'1'}, inplace=True)
entities_pos_rate.to_json('../streamlit_summary_web/data/data_entities_pos_rate_environment.json', force_ascii=False)

### Society
entities_sen_news_society = manipulate_entities(tag = 'company_all', n = 1, df_sen_ner = df_society_ner.copy())
entities_sen_news_society.reset_index(drop = True, inplace = True)
# replace symbol of companies with their names
for i in range(len(entities_sen_news_society)):
    if entities_sen_news_society.loc[i, 'entities'] in sp500.Symbol.tolist():
        entities_sen_news_society.loc[i, 'entities'] = sp500.loc[sp500.Symbol == entities_sen_news_society.loc[i, 'entities'], 'name_clean'].values[0]
# drop duplicates (in case there's one entity in two tags at the same time)
entities_sen_news_society.drop_duplicates(ignore_index = True, inplace = True)
entities_sen_news_society.to_json('../data/entities_sen_news_society.json', force_ascii=False)
#### calculate positive rate...
entities_pos_rate = entities_sen_news_society.groupby(by = ['entities', 'category', 'sentiment']).count().reset_index().pivot_table(index = ['entities', 'category'], columns = 'sentiment', values = 'news_id', fill_value = 0).reset_index()
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
entities_pos_rate.rename(columns = {-1:'-1', 0:'0', 1:'1'}, inplace=True)
entities_pos_rate.to_json('../streamlit_summary_web/data/data_entities_pos_rate_society.json', force_ascii=False)
