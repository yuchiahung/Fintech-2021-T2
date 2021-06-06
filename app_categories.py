import pandas as pd
import numpy as np
from datetime import datetime
import json
import streamlit as st
import re
from PIL import Image
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import plotly.express as px
import word_cloud
import summarized_news

def app(s):
    st.title('MY FAVORITE')
    company_table = pd.read_csv('data/constituents_csv.csv')
    company_table.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in company_table.Name]
    company_table.loc[:, 'name_full'] = ['+'.join(n.split(' ')) for n in company_table.Name]
    industry = company_table.Sector.unique().tolist()
    selection = st.beta_expander('Settings', False)
    with selection:
        st.subheader("Selections")
        col1, col2 = st.beta_columns((3, 1))
        all = st.checkbox('Select All')
        if all:
            s.multiselect = col1.multiselect("Select Your Favorite Categories:", industry, industry)
        else:
            s.multiselect = col1.multiselect("Select Your Favorite Categories:", industry, s.multiselect)
        n_news = col2.number_input("Select Number of News:", min_value = 1, max_value = 20, value = 5, step = 1)
    #session.multiselect
    page_dashboard(s, company_table, n_news)

def page_dashboard(s, company_table, n_news):
    
    #st.header("Dashboard")
    st.subheader('My Selections')
    show = '| '
    for i in s.multiselect:
        show = show + i + ' | '
    st.write(show) if show != '| ' else st.write('Please Select Your Favorite Categories')

    df = pd.read_json('data/data_ner.json')
    company_table = company_table.rename(columns = {'name_clean': 'company'})
    #st.write(company_table)
    df = pd.merge(df, company_table, how = 'left', on = ['company'])
    # all selected categories news
    display_df = df.loc[df.Sector.isin(s.multiselect)]
    # plot wordcloud
    col1, col2 = st.beta_columns((1,4))
    if len(display_df) == 0:
        st.write('Please select at least one category...')
    else:
        # pie plot: positive rate
        rate_list = display_df.groupby('sentiment').count()['id'].tolist()
        fig = px.pie(values = rate_list, names = ['positive', 'neutral', 'negative'],
            hole = .3, 
            color = ['positive', 'neutral', 'negative'],
            color_discrete_map={
                "positive": "#9AC1AE",
                "neutral": "#F2CF92",
                "negative": "#E79C88"
                }
            ) 
        fig.update_layout(autosize=False, width=150, height=150, 
                margin=dict(l=5, r=5, b=5, t=5, pad=0),
                showlegend=False
                ) 
        fig.update_traces(textposition='inside', textinfo='percent+label', insidetextorientation='radial')
        col1.plotly_chart(fig)
        # wordcloud (all companies news)
        col2.pyplot(word_cloud.plot_wordcloud(display_df, n_words = 100))
    
        summarized_df = summarized_news.summarized_multiple_news(display_df, n_sen = n_news)
        summarized_df_time = calculate_time(summarized_df)
        for i in range(n_news):
            display_news(summarized_df_time.loc[i, 'header'], summarized_df_time.loc[i, 'content_summary'], 
                        summarized_df_time.loc[i, 'source'], summarized_df_time.loc[i, 'link'], summarized_df_time.loc[i, 'time_ago'],
                        summarized_df_time.loc[i, 'company_all'], summarized_df_time.loc[i, 'sentiment'])

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

def display_news(header, content_summary, source, url, time_ago, company_list, sentiment):
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
                    font-size: 16px;
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
    if sentiment == 1:
        img = Image.open('img/positive.png')
    elif sentiment == 0:
        img = Image.open('img/neutral.png')
    else:
        img = Image.open('img/negative.png')
    
    col2.image(img, width=70)