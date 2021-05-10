import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

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
                    fontWeight: "bold";
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
    col1.plotly_chart(fig)
    # header & link
    s_all = [1, 0, -1]
    for s in s_all:
        en_s_df = sentiment[(sentiment.entities == entity) & (sentiment.sentiment == s)]
        if len(en_s_df) > 0:
            header, link = news.loc[news.id == en_s_df.sample(1).news_id.values[0], ['header', 'link']].values[0]
            if s == 1:
                col2.markdown(f'<a style="font-size: 14px; color: #495057;background-color: #B3D0C2" href="{link}" target="_blank">{header}</a>', unsafe_allow_html=True)
            elif s == 0:
                col2.markdown(f'<a style="font-size: 14px; color: #495057;background-color: #F6DEB6" href="{link}" target="_blank">{header}</a>', unsafe_allow_html=True)
            else:
                col2.markdown(f'<a style="font-size: 14px; color: #495057;background-color: #F1C7BB" href="{link}" target="_blank">{header}</a>', unsafe_allow_html=True)

def app():
    # df_positive = pd.read_json('test_positive_rate.json')
    df_positive = pd.read_json('test_positive_rate_person_org.json')
    df_sentiment_news = pd.read_json('test_sentiment_entities_person_org.json')
    df_news = pd.read_json('test_data.json')
    for i in range(len(df_positive)):
        ent = df_positive.loc[i, 'entities']
        display_rate(entity = ent, 
                    news = df_news,
                    sentiment = df_sentiment_news,
                    # rate_list = df_positive.loc[i, ['positive_rate', 'neutral_rate', 'negative_rate']].tolist())
                    rate_list = df_positive.loc[i, ['1', '0', '-1']].tolist())
        df_sentiment_news[df_sentiment_news.entities == ent]

    
