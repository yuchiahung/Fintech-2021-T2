import streamlit as st
# import plotly.graph_objs as go
from datetime import datetime
# from plotly.subplots import make_subplots
import pandas as pd
# from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import word_cloud
# import webbrowser
from app_ppt import (ppt_insert_first_title, ppt_insert_summarization, ppt_insert_images)

ppt_insert_first_title(ppt_file='summary.pptx', insert_title='Summary', insert_author='Fintech-2021-T2')
#summarized_text = [('AAA',0.5),('BBB',0.34),('CCC',0.9)]
ppt_insert_summarization(ppt_file='summary.pptx', insert_title='RPA - SUMMY_TITLE', summarized_text= summarized_text)
image_profiles=[('Sentiment Analysis - Company','img/sentiment.jpg'), ('source1', 'img/source1.jpg'), ('source2', 'img/source2.jpg')]
ppt_insert_images(ppt_file='summary.pptx', image_profiles=image_profiles, start_ppt=True)

#利用st.cache()快取沒有改變過的data
# @st.cache()

def select_news(data, n):
    """select n most important/latest summarized news  & calculate time"""
    # sort by time (display latest news)
    data.sort_values(by = 'time', ignore_index = True, ascending = False, inplace = True)
    # remove empty content news
    data.content_summary.replace('', float('NaN'), inplace=True)
    data.dropna(subset = ['content_summary'], inplace = True)
    # remove news which are not related to S&P 500 companies
    data = data[data.company_len > 0]
    # remove biased news & select top n news
    df = data[data.bias.isna()][:n]
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

def display_news(header, content_summary, source, url, time_ago, company_list, sentiment, bias, content):
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
                    font-size: 14px;
                    font-weight: bold;
                    line-height: 2;
                    text-align: center;
                    border: 2px solid #5791a1;
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
    # image of sentiment
    if sentiment == 1:
        img = Image.open('img/positive.png')
    elif sentiment == 0:
        img = Image.open('img/neutral.png')
    else:
        img = Image.open('img/negative.png')
    # col2.image(img, width=70)
    # image of bias
    empty_img = Image.open('img/empty.png')
    if bias == 1:
        bias_img = Image.open('img/like.png')
        col2.image([img, empty_img, bias_img], width=60)
    elif bias == -1:
        bias_img = Image.open('img/dislike.png')
        col2.image([img, empty_img, bias_img], width=60)
    else: 
        col2.image(img, width=60)
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
                            colormap=newcmp, stopwords=stopwords, max_words=70).generate(content)
        # Display the generated image
        fig = plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(fig)

    # separate bar
    # st.markdown('---')

def app():
    # st.image('./icon.png')
    st.title('Latest Unbiased News')
    # read summarized news
    data_news = pd.read_json('data/data_bias_news.json')
    # st.dataframe(df)
    # st.table(data)

    # ----------- wordcloud ----------- #
    st.pyplot(word_cloud.plot_wordcloud(data_news, n_words = 100, date = datetime(2021,5,30)))

    # ----------- summary ----------- #
    topn_news_df = select_news(data_news, n = 15)
    for i in range(len(topn_news_df)):
        display_news(topn_news_df.loc[i, 'header'], topn_news_df.loc[i, 'content_summary'], 
                    topn_news_df.loc[i, 'source'], topn_news_df.loc[i, 'link'], topn_news_df.loc[i, 'time_ago'],
                    topn_news_df.loc[i, 'company_all'], topn_news_df.loc[i, 'sentiment'],
                    topn_news_df.loc[i, 'bias'], topn_news_df.loc[i, 'content'])

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