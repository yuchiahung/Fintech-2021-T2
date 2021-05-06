import streamlit as st
# import plotly.graph_objs as go
from datetime import datetime
# from plotly.subplots import make_subplots
import json
import pandas as pd
# from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt
# from summarizer import Summarizer
# from transformers import AutoTokenizer, AutoConfig, AutoModel
import webbrowser


#利用st.cache()快取沒有改變過的data
@st.cache()
def get_data(date):
    """ Manipulating data as dataframe"""
    df = pd.read_json('test_data.json')
    # to lower-cased
    df['content_lower'] = [text.lower() for text in df['content']]
    # combine header & content (for wordcloud)
    df['all_text'] = df['header'] + ' ' + df['content']
    # convert "time" to datetime data
    df['time'] = pd.to_datetime(df['time'], format = '%Y/%m/%d %H:%M')
    return df

def wordcloud(text, n_words=100):
    # read stopwords
    with open('stopwords_en.txt') as f:
        stopwords = [line.rstrip() for line in f]
    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=150, background_color='white', colormap='ocean', stopwords=stopwords, max_words=n_words).generate(text)
    # Display the generated image
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return fig

def select_news(n):
    """select n most important/lastest summarized news  & calculate time"""
    # read summarized news
    data = pd.read_json('test_summary_data.json')
    ### ----- do something to sort ----- ###
    df = data[:n]
    df.reset_index(inplace = True, drop = True)
    # calculate news published time from now
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['seconds_from_now'] = [(datetime.now() - t).total_seconds() for t in df['time']]
    for i in range(len(df)):
        seconds = df.loc[i, 'seconds_from_now'] 
        if seconds < 60:
            time_ago = f'{int(seconds)} seconds ago'
        elif seconds < 60*60:
            time_ago = f'{int(seconds//60)} minutes ago'
        elif seconds < 60*60*24:
            time_ago = f'{int(seconds//(60*60))} hours ago'
        elif seconds < 60*60*24*7:
            time_ago = f'{int(seconds//(60*60*24))} days ago'
        elif seconds < 60*60*24*30:
            time_ago = f'{int(seconds//(60*60*24*7))} weeks ago'
        elif seconds < 60*60*24*365:
            time_ago = f'{int(seconds//(60*60*24*30))} months ago'
        else:
            time_ago = f'{int(seconds//(60*60*24*365))} years ago'
        df.loc[i, 'time_ago'] = time_ago
    return df


# @st.cache()
# def summarize_news(data, n_news = 10, n_sen = 2):
#     """summarize top n news"""
#     # select top n news
#     selected_news_df = select_news(data, n_news)
#     # selected contents
#     text = selected_news_df['content_lower'].tolist()
#     # get model
#     modelName = "bert-base-uncased" # lower-cased
#     custom_config = AutoConfig.from_pretrained(modelName)
#     custom_config.output_hidden_states=True
#     custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
#     custom_model = AutoModel.from_pretrained(modelName, config=custom_config)
#     model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
#     # summarized contents
#     selected_news_df['content_summary'] = [model(t, num_sentences = n_sen) for t in text]
#     return selected_news_df

def display_news(header, content, source, url, time_ago):
    # clicked = st.button('Original New')
    # if st.button('Original New'):
        # webbrowser.open_new_tab(url)
    st.markdown("""
                <style>
                .small-font {
                    font-size: 10px;
                    color: #7a7c87;
                }
                .news-header {
                    font-size: 20px;
                    color: #5791a1;
                }
                .news-content {
                    font-size: 16px;
                }
                </style>
                """, unsafe_allow_html=True)
    # header & link
    st.markdown(f'<a style="font-size: 20px; color: #5791a1;" href="{url}" target="_blank">{header}</a>', unsafe_allow_html=True)
    # time & source
    st.markdown(f'<p class="small-font">{time_ago} | {source}</p>', unsafe_allow_html=True)
    # content & link to original new
    # st.markdown(f'\n{content}[...](url)', unsafe_allow_html=True)  
    st.markdown(f'<p class="news-content">\n{content}</p>', unsafe_allow_html=True)  
    # add something in expander
    # st.beta_expander('More')
    # separate bar
    st.markdown('---')

def app():
    # st.image('./icon.png')
    st.title('Selected News')
    today = datetime.today().date()
    df = get_data(today)
    # st.dataframe(df)
    # st.table(data)

    # ----------- wordcloud ----------- #
    all_text = ' '.join(df['all_text'])
    st.pyplot(wordcloud(all_text, n_words = 100))

    # ----------- summary ----------- #
    topn_news_df = select_news(n = 15)
    for i in range(len(topn_news_df)):
        display_news(topn_news_df.loc[i, 'header'], topn_news_df.loc[i, 'content_summary'], 
                    topn_news_df.loc[i, 'source'], topn_news_df.loc[i, 'link'], topn_news_df.loc[i, 'time_ago'])

# # st.beta_container()
# # st.beta_columns(spec)
# col1, col2 = st.beta_columns(2)
# col1.subheader('Columnisation')
# st.beta_expander('Expander')
# with st.beta_expander('Expand'):
#     st.write('Juicy deets')
# my_expander = st.beta_expander()
# my_expander.write('Hello there!')
# clicked = my_expander.button('Click me!')