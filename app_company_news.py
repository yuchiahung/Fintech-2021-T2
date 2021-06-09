import pandas as pd
import re
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image
from datetime import datetime
import word_cloud
import summarized_news

def calculate_time(df):
    """calculate time"""
    df.reset_index(drop = True, inplace = True)
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

def display_news(header, content_summary, source, url, time_ago, sentiment, company_list):
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

    # image of sentiment
    if sentiment == 1:
        img = Image.open('img/positive.png')
    elif sentiment == 0:
        img = Image.open('img/neutral.png')
    else:
        img = Image.open('img/negative.png')
    col2.image(img, width=60)

def app():
    st.title('Companies News')
    # read datas
    data_ner = pd.read_json('data/data_ner.json')
    data_ner.sort_values(by = 'time', ascending = False, inplace = True)
    df_positive = pd.read_json('data/data_entities_pos_rate.json')
    sp500 = pd.read_csv('data/constituents_csv.csv')
    sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]

    # select company & number of results
    col1, col2, _ = st.beta_columns((2,1,2))
    selected_company = col1.selectbox('Select a company...', sp500.name_clean.tolist())
    n_news = col2.number_input('Select number of news...', min_value = 1, max_value = 30, value = 3, step = 1)

    # selected_company news
    i = sp500[sp500.name_clean == selected_company].index[0]
    company_news_df = data_ner[data_ner.company_all.apply(lambda x: (selected_company in x) or (sp500.loc[i, 'Symbol'] in x) or (sp500.loc[i, 'Name'] in x))]
    if len(company_news_df) == 0:
        st.wirte("Sorry, there's no related news.")
    else:
        col1, col2 = st.beta_columns((1,4))
        # pie plot: positive rate
        rate_list = df_positive.loc[df_positive.entities == selected_company, ['1', '0', '-1']].values.tolist()[0]
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
        col2.pyplot(word_cloud.plot_wordcloud(data = company_news_df, n_words = 100))

        company_news_df['time'] = pd.to_datetime(company_news_df.time, unit = 'ms')
        # if nltk_sentiment = sentiment, use nltk_compound to count score 
        company_news_df['score'] = [company_news_df.loc[i, 'nltk_compound'] if company_news_df.loc[i, 'nltk_sentiment'] == company_news_df.loc[i, 'sentiment'] else company_news_df.loc[i, 'compound'] for i in company_news_df.index]
        company_news_df.sort_values(by = 'sentiment', ascending=False, inplace=True)
        # convert int to character (to show on plot)
        company_news_df['sentiment'] = ['positive' if s == 1 else ('negative' if s == -1 else 'neutral') for s in company_news_df.sentiment]
        # expander
        sentiment_expander = st.beta_expander('Sentiment by time')
        with sentiment_expander:
            # plot
            fig = px.scatter(company_news_df, 
                            x = 'time', y = 'score',
                            color = 'sentiment',
                            hover_name = 'header', log_x = False, #size_max = 50,
                            color_discrete_sequence=['seagreen', 'sandybrown', 'salmon'])
            fig.update_traces(marker_size = 10, opacity = 0.7)
            fig.update_layout(autosize=False, width=800, height=300, 
                            margin=dict(l=5, r=5, b=5, t=5, pad=0),
                            showlegend=True
                            )
            st.plotly_chart(fig)

        # summarization
        result_df = summarized_news.summarized_multiple_news(company_news = company_news_df, n_sen = n_news)
        result_df_time = calculate_time(result_df)

        if len(result_df_time) >= n_news:
            r_n_news = n_news
        else:
            r_n_news = len(result_df_time)
    
        for i in range(r_n_news):
            display_news(header = result_df_time.loc[i, 'header'],
                        content_summary = result_df_time.loc[i, 'content_summary'],
                        source = result_df_time.loc[i, 'source'],
                        url = result_df_time.loc[i, 'link'],
                        time_ago = result_df_time.loc[i, 'time_ago'],
                        sentiment = result_df_time.loc[i, 'sentiment'], 
                        company_list = result_df_time.loc[i, 'company_all'])