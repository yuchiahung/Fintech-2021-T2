import pandas as pd
import numpy as np
import re

# read datas
all_ner = pd.read_json('../streamlit_summary_web/data/data_ner.json')
sp500 = pd.read_csv('../streamlit_summary_web/data/constituents_csv.csv')
sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]

# biased news (if nltk_compound > pctl90 or < pctl10, would be marked as biased news)
source_score_all = pd.DataFrame()
for i, company in enumerate(sp500.name_clean):
    # print(i, company)
    company_news = all_ner[all_ner.company_all.apply(lambda x: (company in x) or (sp500.loc[i, 'Symbol'] in x) or (sp500.loc[i, 'Name'] in x))]
    source_score = company_news.groupby('source').mean()[['compound', 'nltk_compound']].reset_index()
    if len(source_score) != 0:
        source_score['company'] = company
        source_score['pctl10'] = np.percentile(source_score.nltk_compound, 10)
        source_score['pctl90'] = np.percentile(source_score.nltk_compound, 90)
        source_score['bias'] = [1 if source_score.loc[j, 'nltk_compound'] > source_score.loc[j, 'pctl90'] else (-1 if source_score.loc[j, 'nltk_compound'] < source_score.loc[j, 'pctl10'] else 0) for j in range(len(source_score))]
        # source_score[source_score.bias != 0]
        source_score_all = pd.concat([source_score_all, source_score])
source_score_all.reset_index(drop = True).to_json('source_score_all.json')

bias_source = source_score_all[source_score_all.bias != 0].reset_index(drop = True)
bias_source.to_json('../streamlit_summary_web/data/data_bias_source.json')

# join biased mark to "data_ner.json"

data_ner = pd.read_json('../streamlit_summary_web/data/data_ner.json')
data_ner['ner_company'] = data_ner['company_all']
data_ner_exploded = data_ner.explode('ner_company')
data_ner_exploded.drop_duplicates(subset = ['header', 'source', 'time', 'content', 'link', 'ner_company'], inplace=True)
data_bias = data_ner_exploded.merge(bias_source[['source', 'company', 'bias']], how = 'left', left_on=['source', 'ner_company'], right_on=['source', 'company'])
data_bias.drop_duplicates(subset = ['header', 'source', 'time', 'content', 'link', 'bias'], inplace=True)
data_bias.drop(columns = ['ner_company', 'company_x', 'company_y'], inplace=True)
data_bias.to_json('../streamlit_summary_web/data/data_bias_news.json')

# data_bias_biased = data_bias[data_bias.bias.notna()]
# data_bias_biased.groupby('id').count()[data_bias_biased.groupby('id').count()['header'] > 1]
