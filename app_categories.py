import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import re
import plotly.express as px
import word_cloud
import summarized_news
import manipulate_news

def app(s):
    st.title('MY FAVORITE')
    company_table = pd.read_csv('data/constituents_csv.csv')
    company_table.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in company_table.Name]
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

    df = pd.read_json('data/data_bias_news.json')
    # news in this week
    df['time'] = pd.to_datetime(df.time, unit = 'ms')
    # df_week = df[df.time >= datetime.today() - timedelta(days=7)]
    df_week = df[df.time >= df.time.max() - timedelta(days=7)]
    # manipulate company name (explode)
    df_week['company'] = df_week.company_all.copy()
    df_exploded = df_week.explode('company')
    df_exploded.dropna(subset = ['company'], inplace = True)
    # replace Symbol & full name with clean name
    df_exploded.company_all.replace(company_table.Symbol.tolist(), company_table.name_clean.tolist(), inplace = True)
    df_exploded.company_all.replace(company_table.Name.tolist(), company_table.name_clean.tolist(), inplace = True)
    #st.write(company_table)
    # merge with sector
    df_exploded = df_exploded.merge(company_table, how = 'left', left_on = 'company', right_on = 'name_clean')
    # all selected categories news
    display_df = df_exploded.loc[df_exploded.Sector.isin(s.multiselect)]
    display_df.drop_duplicates(subset = ['header'], inplace = True)
    # plot wordcloud
    col1, col2 = st.beta_columns((1,4))
    if len(display_df) == 0:
        # st.write('Please select at least one category...')
        pass
    else:
        # pie plot: positive rate
        rate_count = display_df.groupby('sentiment').count()['id'].reset_index()
        if len(rate_count) == 3:
            rate_count.sort_values(by = 'sentiment', ascending = False, inplace = True)
            rate_list = rate_count.id.tolist()
        else:
            for s in [-1, 0, 1]:
                if s not in rate_count.sentiment.tolist():
                    rate_count = rate_count.append({'sentiment': s, 'id': 0}, ignore_index=True)
            rate_count.sort_values(by = 'sentiment', ascending = False, inplace = True)
            rate_list = rate_count.id.tolist()

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
        summarized_df_time = manipulate_news.calculate_time(summarized_df)
        if len(summarized_df_time) >= n_news:
            r = n_news
        else:
            r = len(summarized_df_time)
        for i in range(r):
            manipulate_news.display_news(summarized_df_time.loc[i, 'header'], summarized_df_time.loc[i, 'content_summary'], 
                                        summarized_df_time.loc[i, 'source'], summarized_df_time.loc[i, 'link'], summarized_df_time.loc[i, 'time_ago'],
                                        summarized_df_time.loc[i, 'company_all'], summarized_df_time.loc[i, 'sentiment'], 
                                        summarized_df_time.loc[i, 'content'])
