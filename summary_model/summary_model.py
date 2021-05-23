from datetime import datetime
import json
import pandas as pd
from summarizer import Summarizer
from transformers import AutoTokenizer, AutoConfig, AutoModel
import re

def get_data(date):
    """ Manipulating data as dataframe"""
    df = pd.read_json('../streamlit_summary_web/data/data_headlines.json')
    df.drop_duplicates(subset=['header', 'source', 'time', 'content', 'link'], ignore_index = True, inplace = True)
    # to lower-cased
    # df['content_lower'] = [text.lower() for text in df['content']]
    # convert "time" to datetime data
    df['time'] = pd.to_datetime(df['time'], format = '%Y-%m-%dT%H:%M:%SZ')
    # cleaning `header` (remove source name in header)
    df['header'] = [re.sub(' - ' + df.loc[i, 'source'] + '$', '', df.loc[i, 'header']) for i in range(len(df))]
    df['header'] = [re.sub('\s-\s.{2,25}$', '', df.loc[i, 'header']) for i in range(len(df))]
    df['header'] = [re.sub('\s\|\s.{2,12}$', '', df.loc[i, 'header']) for i in range(len(df))]
    return df

def summarize_news(n_sen = 2, previous_summary = pd.DataFrame(columns = ['header'])):
    """summarize all news"""
    # read data
    today = datetime.today().date()
    df = get_data(today)
    # if there's old summary data, we only need to summarize new data
    df_new = df[~df.header.isin(previous_summary.header)]
    # selected contents
    text = df_new['content'].tolist()
    # get model
    modelName = "bert-base-uncased" # lower-cased
    custom_config = AutoConfig.from_pretrained(modelName)
    custom_config.output_hidden_states=True
    custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
    custom_model = AutoModel.from_pretrained(modelName, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
    # summarized contents
    df_new['content_summary'] = [model(t, num_sentences = n_sen) for t in text]
    all_summary = pd.concat([previous_summary, df_new], axis = 0)
    return all_summary

# if there's old summary data, read it
try:
    previous_summary_data = pd.read_json('../streamlit_summary_web/data/data_summary.json')
    data_summary = summarize_news(n_sen=1, previous_summary = previous_summary_data)
except:
    data_summary = summarize_news(n_sen=1)    
# export summarized news
data_summary.to_json('../streamlit_summary_web/data/data_summary.json', force_ascii=False)
