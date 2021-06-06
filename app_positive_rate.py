import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import re


def display_rate(entity, news, sentiment, rate_list = [0.2, 0.2, 0.6]):
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
                .entity-name {
                    font-size: 24px;
                    color: #5791a1;
                    font-weight: bold;
                }
                .header-positive {
                    font-size: 26px;
                    color: #64917d;
                    font-weight: bold;
                    text-align: center;
                    border: 1px solid #64917d;
                    line-height: 2.5;
                    background-color: #d8e3de; 
                }       
                .header-negative {
                    font-size: 26px;
                    color: #c96d55;
                    font-weight: bold;
                    text-align: center;
                    border: 1px solid #c96d55;
                    line-height: 2.5;
                    background-color: #f7dcd5; 
                }
                .header-2 {
                    font-size: 28px;
                    color: #5c5b5b;
                    font-weight: bold;
                    line-height: 2.5;
                }            
                </style>
                """, unsafe_allow_html=True)
    # entity
    st.markdown(f'<p class = "entity-name">{entity}</p>', unsafe_allow_html=True)

    # 2 columns
    col1, col2 = st.beta_columns((1,4))

    # positive rate donut plot
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
    # header & link
    s_all = [1, 0, -1]
    for s in s_all:
        en_s_df = sentiment[(sentiment.entities == entity) & (sentiment.sentiment == s)]
        if len(en_s_df) > 0:
            header, link = news.loc[news.id == en_s_df.sample(1).news_id.values[0], ['header', 'link']].values[0]
            if s == 1:
                col2.markdown(f'<a style="font-size: 14px; color: #495057;background-color: #d8e3de" href="{link}" target="_blank">{header}</a>', unsafe_allow_html=True)
            elif s == 0:
                col2.markdown(f'<a style="font-size: 14px; color: #495057;background-color: #faeed9" href="{link}" target="_blank">{header}</a>', unsafe_allow_html=True)
            else:
                col2.markdown(f'<a style="font-size: 14px; color: #495057;background-color: #f7dcd5" href="{link}" target="_blank">{header}</a>', unsafe_allow_html=True)

def app():
    st.title('Sentiment Analysis')
    st.markdown('---')
    st.markdown(f'<p class = "header-2">1. By Company</p>', unsafe_allow_html=True)
    # df_positive = pd.read_json('test_positive_rate.json')
    df_positive = pd.read_json('data/data_entities_pos_rate.json')
    df_sentiment_news = pd.read_json('data/data_entities_news.json')
    df_news = pd.read_json('data/data_sentiment.json')
    # sort df_positive data by total news count (50 companies which have most news)
    df_positive_top50_sum = df_positive.sort_values(by = 'sum', ascending = False).reset_index(drop = True)[:50]
    # top5 positive companies
    top5_positive = df_positive_top50_sum.sort_values(by = 'positive_rate', ascending=False)[:5].reset_index(drop = True)
    # top5 negative companies
    df_else = df_positive_top50_sum.sort_values(by = 'positive_rate', ascending=False)[5:]
    top5_negative = df_else.sort_values(by = 'negative_rate', ascending=False)[:5].reset_index(drop = True)
    
    # display selected company
    sp500 = pd.read_csv('data/constituents_csv.csv')
    sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]
    # selected_company = st.selectbox('Select a company...', ['All'] + sp500.name_clean.tolist())
    
    # if selected_company == 'All':
    # display top 10 entities
    # top5 positive 
    st.markdown(f'<p class = "header-positive">5 Companies with Highest Positive Rate</p>', unsafe_allow_html=True)
    for i in range(5):
        ent = top5_positive.loc[i, 'entities']
        display_rate(entity = ent, 
                    news = df_news,
                    sentiment = df_sentiment_news,
                    # rate_list = df_positive_sorted.loc[i, ['positive_rate', 'neutral_rate', 'negative_rate']].tolist())
                    rate_list = top5_positive.loc[i, ['1', '0', '-1']].tolist())
    
    # top5 negative 
    st.markdown('---')
    st.markdown(f'<p class = "header-negative">5 Companies with Highest Negative Rate</p>', unsafe_allow_html=True)
    for i in range(5):
        ent = top5_negative.loc[i, 'entities']
        display_rate(entity = ent, 
                    news = df_news,
                    sentiment = df_sentiment_news,
                    # rate_list = df_positive_sorted.loc[i, ['positive_rate', 'neutral_rate', 'negative_rate']].tolist())
                    rate_list = top5_negative.loc[i, ['1', '0', '-1']].tolist())
    # elif len(df_sentiment_news[df_sentiment_news.entities == selected_company]) == 0:
    #     st.write('Cannot find related news')
    # else:
    #     display_rate(entity = selected_company,
    #                     news = df_news,
    #                     sentiment = df_sentiment_news,
    #                     rate_list = df_positive.loc[df_positive.entities == selected_company, ['1', '0', '-1']].values.tolist()[0])
    #     # extract the news related to selected_company
    #     selected_news_id = df_sentiment_news.loc[df_sentiment_news.entities == selected_company, 'news_id'].tolist()
    #     selected_news = df_news[df_news.id.isin(selected_news_id)]
    #     selected_news['time'] = pd.to_datetime(selected_news.time, unit = 'ms')
    #     # if nltk_sentiment = sentiment, use nltk_compound to count score 
    #     selected_news['score'] = [selected_news.loc[i, 'nltk_compound'] if selected_news.loc[i, 'nltk_sentiment'] == selected_news.loc[i, 'sentiment'] else selected_news.loc[i, 'compound'] for i in selected_news.index]
    #     selected_news.sort_values(by = 'sentiment', ascending=False, inplace=True)
    #     # convert int to character (to show on plot)
    #     selected_news['sentiment'] = ['positive' if s == 1 else ('negative' if s == -1 else 'neutral') for s in selected_news.sentiment]
    #     # plot
    #     fig = px.scatter(selected_news, 
    #                     x = 'time', y = 'score',
    #                     color = 'sentiment',
    #                     hover_name = 'header', log_x = False, #size_max = 50,
    #                     color_discrete_sequence=['seagreen', 'sandybrown', 'salmon'])
    #     fig.update_traces(marker_size = 10, opacity = 0.7)
    #     fig.update_layout(autosize=False, width=800, height=400, 
    #                     margin=dict(l=5, r=5, b=5, t=5, pad=0),
    #                     showlegend=True
    #                     )
    #     st.plotly_chart(fig)
        
    st.markdown('---')
    st.markdown(f'<p class = "header-2">2. By Source</p>', unsafe_allow_html=True)
    df_news['time'] = pd.to_datetime(df_news['time'], unit='ms')  
    df_news['date'] = df_news['time'].dt.date
    # count sentiment of source per day
    source_sen_count = df_news.groupby(by = ['date', 'source', 'sentiment']).count()[['id']].reset_index()
    source_sen_count_p = source_sen_count.pivot(index = ['date', 'source'], columns = 'sentiment', values = 'id').reset_index()
    source_sen_count_p.fillna(0, inplace = True)
    # total news count (in that day)
    source_sen_count_p['sum'] = source_sen_count_p[[-1, 0, 1]].sum(axis = 1)
    # score of the day for every source
    source_sen_count_p['score'] = (source_sen_count_p[1] - source_sen_count_p[-1]) / source_sen_count_p['sum']
    # select top 10 source (which have the most # news)
    top10_source = df_news.groupby('source').count()[['id']].sort_values(by='id', ascending=False)[:10].reset_index()['source'].tolist()
    top10_sen_count = source_sen_count_p[source_sen_count_p.source.isin(top10_source)]

    ### bubble plot: show the sources' sentiment in timeline
    fig = px.scatter(top10_sen_count, 
                    x = 'date', y = 'score',
                    size = 'sum', color = 'source',
                    hover_name = 'source', log_x = False, size_max = 50,
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig)

    ### box plot of score
    fig2 = px.box(top10_sen_count,
                    x = 'source', y = 'score',
                    color = 'source',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig2)