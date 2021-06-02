import pandas as pd
import numpy as np
from datetime import datetime
import json
import streamlit as st
import SessionState
import re
from PIL import Image
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import datetime as dt

def app():

    # Sidebar
    st.title('KEYWORD SEARCH')

    col1,col2,col3 = st.beta_columns(3)
    #search欄位
    with col1:
        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
        selected = st.text_input("", "Search...")

    with col2:
        start_date = st.date_input("Start date", datetime(2019, 1, 1))
    
    with col3:
        end_date = st.date_input("End date", datetime(2021, 6, 1))


    #按紐
    go = st.button('GO')

    if go:
        start = start_date
        end = end_date
        search = selected
        dashboard(search, start, end)


def dashboard(search, start, end):
    df = pd.read_json('data/data_ner.json')
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    company_table = pd.read_csv('data/constituents_csv.csv')
    company_table.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in company_table.Name]
    company_table.loc[:, 'name_full'] = ['+'.join(n.split(' ')) for n in company_table.Name]
    company = company_table.name_clean.tolist()
    if search in company:
        display_df = df.loc[(df.company_all.astype(str).str.contains(search)) & (df.time.dt.date.between(start, end))]
        display_df = display_df.loc[display_df.company_len != 0]
    else:
        display_df = df.loc[(df.content.str.contains(search)) & (df.time.dt.date.between(start, end))]
        display_df = display_df.loc[display_df.company_len != 0]
    display_df = select_news(display_df, n = 15)
    score = round((1 - (display_df.neg.sum() / len(display_df.neg))), 4) * 100
    st.subheader('Sentiment Score：' + str(score))
    #st.write(display_df)

    for i in range(len(display_df)):
        display_news(display_df.loc[i, 'header'], display_df.loc[i, 'content_summary'], 
                    display_df.loc[i, 'source'], display_df.loc[i, 'link'], display_df.loc[i, 'time_ago'],
                    display_df.loc[i, 'company_all'], display_df.loc[i, 'sentiment'],
                    display_df.loc[i, 'content'])


def select_news(data, n):
    """select n most important/latest summarized news  & calculate time"""
    # sort by time (display latest news)
    data.sort_values(by = 'time', ignore_index = True, ascending = False, inplace = True)
    data.content_summary.replace('', float('NaN'), inplace=True)
    data.dropna(subset = ['content_summary'], inplace = True)
    df = data[data.company_len > 0][:n]
    df.reset_index(drop=True, inplace = True)
    # calculate news published time from now
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

    



    
