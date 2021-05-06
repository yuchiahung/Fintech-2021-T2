from datetime import datetime
import json
import pandas as pd
from summarizer import Summarizer
from transformers import AutoTokenizer, AutoConfig, AutoModel

def get_data(date):
    """ Manipulating data as dataframe"""
    df = pd.read_json('../streamlit_summary_web/test_data.json')
    # to lower-cased
    df['content_lower'] = [text.lower() for text in df['content']]
    # combine header & content (for wordcloud)
    df['all_text'] = df['header'] + ' ' + df['content']
    # convert "time" to datetime data
    df['time'] = pd.to_datetime(df['time'], format = '%Y/%m/%d %H:%M')
    return df

def summarize_news(n_sen = 2):
    """summarize all news"""
    # read data
    today = datetime.today().date()
    df = get_data(today)
    # selected contents
    text = df['content_lower'].tolist()
    # get model
    modelName = "bert-base-uncased" # lower-cased
    custom_config = AutoConfig.from_pretrained(modelName)
    custom_config.output_hidden_states=True
    custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
    custom_model = AutoModel.from_pretrained(modelName, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
    # summarized contents
    df['content_summary'] = [model(t, num_sentences = n_sen) for t in text]
    return df

# export summarized news
summarize_news(n_sen=1).to_json('../streamlit_summary_web/test_summary_data.json', force_ascii=False)
