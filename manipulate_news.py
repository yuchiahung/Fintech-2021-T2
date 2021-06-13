import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from PIL import Image
import numpy as np
from wordcloud import WordCloud

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
                            colormap=newcmp, stopwords=stopwords, max_words=70).generate(content)
        # Display the generated image
        fig = plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(fig)

def calculate_time(df):
    """calculate time"""
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

def select_news(data, n):
    """select n most important/latest summarized news  & calculate time"""
    # drop duplicates
    data.drop_duplicates(subset = ['header'], inplace = True)
    # sort by time (display latest news)
    data.sort_values(by = 'time', ignore_index = True, ascending = False, inplace = True)
    # remove empty content news
    data.content_summary.replace('', float('NaN'), inplace=True)
    data.dropna(subset = ['content_summary'], inplace = True)
    # remove news which are not related to S&P 500 companies
    data = data[data.company_len > 0]
    # remove biased news & select top n news
    df = data[data.bias.isna()][:n]
    df = calculate_time(df)
    return df
