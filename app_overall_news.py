import streamlit as st
# import plotly.graph_objs as go
from datetime import datetime, timedelta
# from plotly.subplots import make_subplots
import pandas as pd
# from collections import Counter
import word_cloud
import manipulate_news
# import webbrowser

#利用st.cache()快取沒有改變過的data
# @st.cache()

def app():
    # st.image('./icon.png')
    st.title('Latest Unbiased News')
    # read summarized news
    data_news = pd.read_json('data/data_bias_news.json')
    # st.dataframe(df)
    # st.table(data)

    
    data_news['time_dt'] = pd.to_datetime(data_news['time'], unit='ms')  
    a_week_ago = data_news['time_dt'].max() - timedelta(days=7)
    data_week = data_news[data_news.time_dt > a_week_ago]

    # ----------- wordcloud ----------- #
    st.pyplot(word_cloud.plot_wordcloud(data_week, n_words = 100, date = datetime(2021,6,10)))

    # ----------- summary ----------- #
    topn_news_df = manipulate_news.select_news(data_week, n = 15)
    for i in range(len(topn_news_df)):
        manipulate_news.display_news(topn_news_df.loc[i, 'header'], topn_news_df.loc[i, 'content_summary'], 
                            topn_news_df.loc[i, 'source'], topn_news_df.loc[i, 'link'], topn_news_df.loc[i, 'time_ago'],
                            topn_news_df.loc[i, 'company_all'], topn_news_df.loc[i, 'sentiment'],
                            topn_news_df.loc[i, 'content'])

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