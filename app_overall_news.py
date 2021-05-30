import streamlit as st
# import plotly.graph_objs as go
from datetime import datetime, timedelta
# from plotly.subplots import make_subplots
import json
import pandas as pd
# from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from PIL import Image
# import webbrowser


#利用st.cache()快取沒有改變過的data
# @st.cache()

def wordcloud(data, n_words=100):
    """ Wordcloud of news of the week """
    a_week_ago = datetime.today() - timedelta(days=7)
    data['time'] = pd.to_datetime(data['time'], unit='ms')  
    data_week = data[data.time > a_week_ago]
    text = ' '.join(data_week['header'] + ' ' + data_week['content'])
    # read stopwords
    with open('stopwords_en.txt') as f:
        stopwords = [line.rstrip() for line in f]
    # Generate color map
    oceanBig = cm.get_cmap('ocean', 512)
    newcmp = ListedColormap(oceanBig(np.linspace(0, 0.85, 256)))
    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=150, background_color='white', 
                          colormap=newcmp, stopwords=stopwords, max_words=n_words).generate(text)
    # Display the generated image
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return fig

def select_news(data, n):
    """select n most important/latest summarized news  & calculate time"""
    # sort by time (display latest news)
    data.sort_values(by = 'time', ignore_index = True, ascending = False, inplace = True)
    data.content_summary.replace('', float('NaN'), inplace=True)
    data.dropna(subset = ['content_summary'], inplace = True)
    df = data[data.company_len > 0][:n]
    df.reset_index(drop=True, inplace = True)
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

def display_news(header, content_summary, source, url, time_ago, company_list, sentiment, content):
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
                .company-name {
                    font-size: 18px;
                    font-weight: bold;
                    line-height: 2.5;
                    text-align: center;
                    border: 3px solid #5791a1;
                    color: #5791a1;
                }
                </style>
                """, unsafe_allow_html=True)
    # header & link
    st.markdown(f'<a style="font-size: 20px; color: #5791a1;" href="{url}" target="_blank">{header}</a>', unsafe_allow_html=True)

    # 2 columns
    col1, col2 = st.beta_columns((4,1))
    # time & source
    col1.markdown(f'<p class="small-font">{time_ago} | {source}</p>', unsafe_allow_html=True)
    # content & link to original new
    # st.markdown(f'\n{content}[...](url)', unsafe_allow_html=True)  
    col1.markdown(f'<p class="news-content">{content_summary}</p>', unsafe_allow_html=True)  
    
    # S&P500 company name (if there is)
    for i in range(len(company_list)):
        col2.markdown(f'<p class="company-name">{"  "+company_list[i]}</p>', unsafe_allow_html=True)  
        # if col2.button(company_list[i]):
            # pass
    if sentiment == 1:
        img = Image.open('img/positive.png')
    elif sentiment == 0:
        img = Image.open('img/neutral.png')
    else:
        img = Image.open('img/negative.png')
    
    col2.image(img, width=70)
    # add something in expander
    my_expander = st.beta_expander('Word Cloud')
    with my_expander:
        # read stopwords
        with open('stopwords_en.txt') as f:
            stopwords = [line.rstrip() for line in f]
        # Generate color map
        oceanBig = cm.get_cmap('ocean', 512)
        newcmp = ListedColormap(oceanBig(np.linspace(0, 0.85, 256)))
        # Generate a word cloud image
        wordcloud = WordCloud(width=800, height=150, background_color='white', 
                            colormap=newcmp, stopwords=stopwords, max_words=100).generate(content)
        # Display the generated image
        fig = plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(fig)

    # separate bar
    # st.markdown('---')

def app():
    # st.image('./icon.png')
    st.title('Latest News')
    today = datetime.today().date()
    # read summarized news
    data_ner = pd.read_json('data/data_ner.json')
    # st.dataframe(df)
    # st.table(data)

    # ----------- wordcloud ----------- #
    st.pyplot(wordcloud(data_ner, n_words = 100))

    # ----------- summary ----------- #
    topn_news_df = select_news(data_ner, n = 15)
    for i in range(len(topn_news_df)):
        display_news(topn_news_df.loc[i, 'header'], topn_news_df.loc[i, 'content_summary'], 
                    topn_news_df.loc[i, 'source'], topn_news_df.loc[i, 'link'], topn_news_df.loc[i, 'time_ago'],
                    topn_news_df.loc[i, 'company_all'], topn_news_df.loc[i, 'sentiment'],
                    topn_news_df.loc[i, 'content'])

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