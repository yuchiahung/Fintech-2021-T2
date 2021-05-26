import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def app():
    st.title('Sentiment of News Sources')
    # read data
    df_ner = pd.read_json('data/data_ner.json')
    # to datetime
    # df_ner['time'] = pd.to_datetime(df_ner['time'], format = '%Y-%m-%dT%H:%M:%SZ')
    df_ner['time'] = pd.to_datetime(df_ner['time'], unit='ms')  
    df_ner['date'] = df_ner['time'].dt.date
    # count sentiment of source per day
    source_sen_count = df_ner.groupby(by = ['date', 'source', 'sentiment']).count()[['id']].reset_index()
    source_sen_count_p = source_sen_count.pivot(index = ['date', 'source'], columns = 'sentiment', values = 'id').reset_index()
    source_sen_count_p.fillna(0, inplace = True)
    # total news count (in that day)
    source_sen_count_p['sum'] = source_sen_count_p[[-1, 0, 1]].sum(axis = 1)
    # score of the day for every source
    source_sen_count_p['score'] = (source_sen_count_p[1] - source_sen_count_p[-1]) / source_sen_count_p['sum']
    # select top 10 source (which have the most # news)
    top10_source = df_ner.groupby('source').count()[['id']].sort_values(by='id', ascending=False)[:10].reset_index()['source'].tolist()
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

