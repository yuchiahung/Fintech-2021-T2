import pandas as pd
from datetime import datetime
import streamlit as st
import SessionState
import re
import manipulate_news

def app():

    # Sidebar
    st.title('KEYWORD SEARCH')

    col1,col2,col3 = st.beta_columns(3)
    #search欄位
    with col1:
        # def icon(icon_name):
        #     st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
        selected = st.text_input("", "Search...")

    with col2:
        start_date = st.date_input("Start date", datetime(2021, 4, 1))
    
    with col3:
        end_date = st.date_input("End date", datetime.today())


    #按紐
    go = st.button('GO')

    if go:
        start = start_date
        end = end_date
        search = selected
        dashboard(search, start, end)


def dashboard(search, start, end):
    df = pd.read_json('data/data_bias_news.json')
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    company_table = pd.read_csv('data/constituents_csv.csv')
    company_table.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in company_table.Name]
    company = company_table.name_clean.tolist()
    # only display news about s&p500 companies
    df = df.loc[df.company_len != 0]
    if search in company:
        display_df = df.loc[(df.company_all.astype(str).str.contains(search)) & (df.time.dt.date.between(start, end))]
        display_df.drop_duplicates(subset = ['header'], inplace = True)
        selected_display_df = manipulate_news.select_news(display_df, n = 15)
    else:
        df.drop_duplicates(subset = ['header'], inplace = True)
        display_df_header = df.loc[(df.header.str.contains(search)) & (df.time.dt.date.between(start, end))]
        display_df_content = df.loc[(df.content.str.contains(search)) & (df.time.dt.date.between(start, end))]
        # search header first
        if len(display_df_header) >= 15:
            score = (((display_df_header.sentiment==1).sum() + (display_df_header.sentiment==0).sum()*0.5) / len(display_df_header.sentiment)) * 100
            selected_display_df = manipulate_news.select_news(display_df_header, n = 15)
        # if not enough, search content
        elif len(display_df_header) != 0:
            score = (((display_df_content.sentiment==1).sum() + (display_df_content.sentiment==0).sum()*0.5) / len(display_df_content.sentiment)) * 100
            selected_display_df_content = manipulate_news.select_news(display_df_content, n = 15 - len(display_df_header))
            selected_display_df = pd.concat([display_df_header, selected_display_df_content])
            selected_display_df.drop_duplicates(subset = ['header'], inplace = True)
        # there's no header contains keyword
        else:
            score = (((display_df_content.sentiment==1).sum() + (display_df_content.sentiment==0).sum()*0.5) / len(display_df_content.sentiment))* 100
            selected_display_df = manipulate_news.select_news(display_df_content, n = 15)
        
        selected_display_df.drop_duplicates(subset = ['header'], inplace = True)
    
    st.subheader('Sentiment Score：' + str(round(score, 2)))
    #st.write(display_df)
    selected_display_df.reset_index(drop = True, inplace = True)
    for i in range(len(selected_display_df)):
        manipulate_news.display_news(selected_display_df.loc[i, 'header'], selected_display_df.loc[i, 'content_summary'], 
                                    selected_display_df.loc[i, 'source'], selected_display_df.loc[i, 'link'], selected_display_df.loc[i, 'time_ago'],
                                    selected_display_df.loc[i, 'company_all'], selected_display_df.loc[i, 'sentiment'],
                                    selected_display_df.loc[i, 'content'])



    
