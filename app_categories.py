import pandas as pd
import numpy as np
from datetime import datetime
import json
import streamlit as st
import SessionState

def app(s):
    st.title('MY FAVORITE')
    
    selection = st.beta_expander('Settings', False)
    selection.subheader("Selections")

    options = ['Asia', 'World', 'Commentary', 'Opinion', 'Face Tank', 'Culture']
    s.multiselect = selection.multiselect("Select Your Favorite Categories:", options, options)
    #session.multiselect

    page_dashboard(s)

def page_dashboard(s):
    
    #st.header("Dashboard")
    st.subheader('My Selections')
    show = '| '
    for i in s.multiselect:
        show = show + i + ' | '
    st.write(show) if show != '| ' else st.write('Please Select Your Favorite Categories')

    df = pd.read_json('data/data_summary.json')
    display_df = df.loc[df.category.isin(s.multiselect)]
    display_df = select_news(15,display_df)
    for i in range(len(display_df)):
        display_news(display_df.loc[i, 'header'], display_df.loc[i, 'content_summary'], 
                    display_df.loc[i, 'source'], display_df.loc[i, 'link'], display_df.loc[i, 'time_ago'])
    

def select_news(n, data):
    """select n most important/lastest summarized news  & calculate time"""
    ### ----- do something to sort ----- ###
    df = data[:n]
    df.reset_index(inplace = True, drop = True)
    # calculate news published time from now
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['seconds_from_now'] = [(datetime.now() - t).total_seconds() for t in df['time']]
    time_list = list()
    for i in range(len(df)):
        seconds = df.loc[i,'seconds_from_now'] 
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
        time_list.append(time_ago)
    df['time_ago'] = time_list
    return df

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
