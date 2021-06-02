from datetime import datetime
import json
import pandas as pd
from summarizer import Summarizer
from transformers import AutoTokenizer, AutoConfig, AutoModel
import re

def get_data(date):
    """ Manipulating data as dataframe"""
    df = pd.read_json('../streamlit_summary_web/data/data_sp500.json')
    df.drop_duplicates(subset=df.columns.tolist()[1:], ignore_index = True, inplace = True)
    # to lower-cased
    # df['content_lower'] = [text.lower() for text in df['content']]
    # convert "time" to datetime data
    df['time'] = pd.to_datetime(df['time'], format = '%Y-%m-%dT%H:%M:%SZ')
    # drop na & reset index
    df.dropna(inplace=True)
    df.reset_index(drop = True, inplace=True)
    # cleaning `header` (remove source name in header)
    df['header'] = [re.sub(' - ' + df.loc[i, 'source'] + '$', '', df.loc[i, 'header']) for i in range(len(df))]
    df['header'] = [re.sub('\s-\s.{2,25}$', '', df.loc[i, 'header']) for i in range(len(df))]
    df['header'] = [re.sub('\s\|\s.{2,12}$', '', df.loc[i, 'header']) for i in range(len(df))]
    df['content_len'] = [len(c) for c in df.content]
    df = df[df.content_len > 200]
    df.reset_index(drop = True, inplace=True)
    # clean contents from Yahoo Entertainment
    df['content'] = [re.sub(r'^.{25,50} \-\-', '', df.loc[i, 'content']) if df.loc[i, 'source'] == 'Yahoo Entertainment' else df.loc[i, 'content'] for i in range(len(df))]
    return df

def summarize_news(n_sen = 2, previous_summary = pd.DataFrame(columns = ['header'])):
    """summarize all news"""
    # read data
    today = datetime.today().date()
    df = get_data(today)
    # if there's old summary data, we only need to summarize new data
    df_new = df[~df.header.isin(previous_summary.header)]
    # selected contents
    # text = df_new['content'].tolist()
    # get model
    modelName = "bert-base-uncased" # lower-cased
    custom_config = AutoConfig.from_pretrained(modelName)
    custom_config.output_hidden_states=True
    custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
    custom_model = AutoModel.from_pretrained(modelName, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
    # summarized contents
    # df_new.loc[:, 'content_summary'] = [model(t, num_sentences = n_sen) for t in text]
    df_new.reset_index(drop = True, inplace = True)
    for i in range(len(df_new)):
        df_new.loc[i, 'content_summary'] = model(df_new.loc[i, 'content'], num_sentences = n_sen)
        # save file every 200 news
        if i % 200 == 0:
            df_new.to_json('../streamlit_summary_web/data/data_summary_temp.json', force_ascii=False)
    all_summary = pd.concat([previous_summary, df_new], axis = 0)
    return all_summary
"""
%%time
for i in range(2100, 2100):
    df_new.loc[i, 'content_summary'] = model(df_new.loc[i, 'content'], num_sentences = n_sen)
    if i%100 == 0:
        df_new.to_json('../streamlit_summary_web/data/data_summary.json', force_ascii=False)
"""

# if there's old summary data, read it
try:
    previous_summary_data = pd.read_json('../streamlit_summary_web/data/data_summary.json')
    data_summary = summarize_news(n_sen=1, previous_summary = previous_summary_data)
except:
    data_summary = summarize_news(n_sen=1)
# export summarized news
data_summary.reset_index(drop = True, inplace = True)
data_summary.to_json('../streamlit_summary_web/data/data_summary.json', force_ascii=False)
