from typing import KeysView
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import re

def app():
    st.title('ESG Media Trend')
    # search = st.beta_expander('Search', False)

    col1,col2,_ = st.beta_columns((1,1,1))
    topic_option = ["Environment", "Society"]
    environment_option = ["All", "sustainable development", "climate change", "marine ecology", "carbon emission"]
    society_option = ["All", "human right","Racial discrimination","Social engagement","gap between rich and poor","Religious Conflicts"]
    with col1:
        selected_topic = st.selectbox("Please select a topic", options=topic_option)
    
    with col2:
        if selected_topic == "Environment":
            selected_issue = st.selectbox("Please select an issue", environment_option)
        if selected_topic == "Society":
            selected_issue = st.selectbox("Please select an issue", society_option)

    df = pd.read_json('df.json')
    df_2 = pd.read_json('df_2.json')

    df3 = df[0:800]
    delete = [0,None]
    boolean_series = ~df3['head'].isin(delete)
    df3 = df3[boolean_series]
    df4 = df3[df3['head'].str.contains('EU')]
    df5 = df3[df3['head'].str.contains('UN')]
    df6 = df3[df3['head'].str.contains('Microsoft')]
    df7 = df3[df3['head'].str.contains('NASDAQ')]
    df8 = df3[df3['head'].str.contains('JPM')]
    df9 = pd.concat([df4,df5,df6,df7,df8])
    df10 = df9.reset_index(drop=True)
    for i, row in df10.iterrows():
        if int (i) <=8:
            df10.loc[i, 'organize_name']='EU'
        elif int (i) <=16:
            df10.loc[i, 'organize_name']='UN'
        elif int (i) <=19:
            df10.loc[i, 'organize_name']='Microsoft'
        elif int (i) <=22:
            df10.loc[i, 'organize_name']='NASDAQ'
        elif int (i) <=26:
            df10.loc[i, 'organize_name']='JPM'

    df11 = df[800:1600]
    delete = [0,None]
    boolean_series = ~df11['head'].isin(delete)
    df11 = df11[boolean_series]
    df12 = df11[df11['head'].str.contains('EU')]
    df13 = df11[df11['head'].str.contains('Reuters')]
    df14 = df11[df11['head'].str.contains('GOP')]
    df15 = df11[df11['head'].str.contains('EPA')]
    df16 = df11[df11['head'].str.contains('Navy')]
    df17 = pd.concat([df12,df13,df14,df15,df16])
    df18 = df17.reset_index(drop=True)
    for i, row in df18.iterrows():
        if int (i) <=23:
            df18.loc[i, 'organize_name']='EU'
        elif int (i) <=40:
            df18.loc[i, 'organize_name']='Reuters'
        elif int (i) <=52:
            df18.loc[i, 'organize_name']='GOP'
        elif int (i) <=62:
            df18.loc[i, 'organize_name']='EPA'
        elif int (i) <=64:
            df18.loc[i, 'organize_name']='Navy'
    df19 = df[1600:2400]
    delete = [0,None]
    boolean_series = ~df19['head'].isin(delete)
    df19 = df19[boolean_series]
    df20 = df19[df19['head'].str.contains('Pentagon')]
    df21 = df19[df19['head'].str.contains('Navy')]
    df22 = df19[df19['head'].str.contains('Marines')]
    df23 = df19[df19['head'].str.contains('EU')]
    df24 = df19[df19['head'].str.contains('Reuters')]
    df25 = pd.concat([df20,df21,df22,df23,df24])
    df26 = df25.reset_index(drop=True)
    for i, row in df26.iterrows():
        if int (i) <=6:
            df26.loc[i, 'organize_name']='Pentagon'
        elif int (i) <=17:
            df26.loc[i, 'organize_name']='Navy'
        elif int (i) <=25:
            df26.loc[i, 'organize_name']='Marines'
        elif int (i) <=30:
            df26.loc[i, 'organize_name']='EU'
        elif int (i) <=35:
            df26.loc[i, 'organize_name']='Reuters'
    df27 = df[2400:3200]
    delete = [0,None]
    boolean_series = ~df27['head'].isin(delete)
    df27 = df27[boolean_series]
    df28 = df27[df27['head'].str.contains('Reuters')]
    df29 = df27[df27['head'].str.contains('EU')]
    df30 = df27[df27['head'].str.contains('Daimler')]
    df31 = df27[df27['head'].str.contains('Hyundai')]
    df32 = df27[df27['head'].str.contains('IEA')]
    df33 = pd.concat([df28,df29,df30,df31,df32])
    df34 = df33.reset_index(drop=True)
    for i, row in df34.iterrows():
        if int (i) <=24:
            df34.loc[i, 'organize_name']='Reuters'
        elif int (i) <=34:
            df34.loc[i, 'organize_name']='EU'
        elif int (i) <=42:
            df34.loc[i, 'organize_name']='Daimler'
        elif int (i) <=50:
            df34.loc[i, 'organize_name']='Hyundai'
        elif int (i) <=58:
            df34.loc[i, 'organize_name']='IEA'   
    df35 = df_2[0:800]
    delete = [0,None]
    boolean_series = ~df35['head'].isin(delete)
    df35 = df35[boolean_series]
    df36 = df35[df35['head'].str.contains('Associated Press')]
    df37 = df35[df35['head'].str.contains('QAnon')]
    df38 = df35[df35['head'].str.contains('CNN')]
    df39 = df35[df35['head'].str.contains('Reuters')]
    df40 = df35[df35['head'].str.contains('Yale')]
    df41 = pd.concat([df36,df37,df38,df39,df40])
    df42 = df41.reset_index(drop=True)
    for i, row in df42.iterrows():
        if int (i) <=31:
            df42.loc[i, 'organize_name']='Associted Press'
        elif int (i) <=47:
            df42.loc[i, 'organize_name']='QAnon'
        elif int (i) <=63:
            df42.loc[i, 'organize_name']='CNN'
        elif int (i) <=79:
            df42.loc[i, 'organize_name']='Reuters'
        elif int (i) <=95:
            df42.loc[i, 'organize_name']='Yale'
    df43 = df_2[800:1600]
    delete = [0,None]
    boolean_series = ~df43['head'].isin(delete)
    df43 = df43[boolean_series]
    df44 = df43[df43['head'].str.contains('NFL')]
    df45 = df43[df43['head'].str.contains('USDA')]
    df46 = df43[df43['head'].str.contains('Amazon')]
    df47 = df43[df43['head'].str.contains('McDonald')]
    df48 = df43[df43['head'].str.contains('Hawkeyes')]
    df49 = pd.concat([df44,df45,df46,df47,df48])
    df50 = df49.reset_index(drop=True)
    for i, row in df50.iterrows():
        if int (i) <=16:
            df50.loc[i, 'organize_name']='NFL'
        elif int (i) <=23:
            df50.loc[i, 'organize_name']='USDA'
        elif int (i) <=34:
            df50.loc[i, 'organize_name']='Amazon'
        elif int (i) <=41:
            df50.loc[i, 'organize_name']='McDonald'
        elif int (i) <=46:
            df50.loc[i, 'organize_name']='Hawkeyes'
    df51 = df_2[1600:2400]
    delete = [0,None]
    boolean_series = ~df51['head'].isin(delete)
    df51 = df51[boolean_series]
    df52 = df51[df51['head'].str.contains('Billboard Awards')]
    df53 = df51[df51['head'].str.contains('Facebook')]
    df54 = df51[df51['head'].str.contains('CDC')]
    df55 = df51[df51['head'].str.contains('UN')]
    df56 = df51[df51['head'].str.contains('Social Services')]
    df57 = pd.concat([df52,df53,df54,df55,df56])
    df58 = df57.reset_index(drop=True)
    for i, row in df58.iterrows():
        if int (i) <=14:
            df58.loc[i, 'organize_name']='Billboard Awards'
        elif int (i) <=25:
            df58.loc[i, 'organize_name']='Facebook'
        elif int (i) <=29:
            df58.loc[i, 'organize_name']='CDC'
        elif int (i) <=35:
            df58.loc[i, 'organize_name']='UN'
        elif int (i) <=38:
            df58.loc[i, 'organize_name']='Social Services'
    df59 = df_2[2400:3200]
    delete = [0,None]
    boolean_series = ~df59['head'].isin(delete)
    df59 = df59[boolean_series]
    df60 = df59[df59['head'].str.contains('WTO')]
    df61 = df59[df59['head'].str.contains('AFT')]
    df62 = df59[df59['head'].str.contains('Reuters')]
    df63 = df59[df59['head'].str.contains('UN')]
    df64 = df59[df59['head'].str.contains('Covid-19')]
    df65 = pd.concat([df60,df61,df62,df63,df64])
    df66 = df65.reset_index(drop=True)
    for i, row in df66.iterrows():
        if int (i) <=5:
            df66.loc[i, 'organize_name']='WTO'
        elif int (i) <=6:
            df66.loc[i, 'organize_name']='AFT'
        elif int (i) <=9:
            df66.loc[i, 'organize_name']='Reuters'
        elif int (i) <=12:
            df66.loc[i, 'organize_name']='UN'
        elif int (i) <=35:
            df66.loc[i, 'organize_name']='Covid-19'
    df67 = df_2[3200:4000]
    delete = [0,None]
    boolean_series = ~df67['head'].isin(delete)
    df67 = df67[boolean_series]
    df68 = df67[df67['head'].str.contains('Hamas')]
    df69 = df67[df67['head'].str.contains('NATO')]
    df70 = df67[df67['head'].str.contains('UN')]
    df71 = df67[df67['head'].str.contains('COVID')]
    df72 = df67[df67['head'].str.contains('GOP')]
    df73 = pd.concat([df68,df69,df70,df71,df72])
    df74 = df73.reset_index(drop=True)
    for i, row in df74.iterrows():
        if int (i) <=15:
            df74.loc[i, 'organize_name']='Hamas'
        elif int (i) <=18:
            df74.loc[i, 'organize_name']='NATO'
        elif int (i) <=21:
            df74.loc[i, 'organize_name']='UN'
        elif int (i) <=31:
            df74.loc[i, 'organize_name']='COVID'
        elif int (i) <=33:
            df74.loc[i, 'organize_name']='GOP'

    fig = px.box(df,
                    x = 'category', y = 'nltk_compound',
                    color = 'category',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig2 = px.box(df_2,
                    x = 'category', y = 'nltk_compound',
                    color = 'category',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig3 = px.box(df10,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig4 = px.box(df18,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig5 = px.box(df26,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig6 = px.box(df34,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig7 = px.box(df42,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig8 = px.box(df50,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig9 = px.box(df58,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig10 = px.box(df66,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 

    fig11 = px.box(df74,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    
    if (selected_topic == "Environment") & (selected_issue == "All"):
        st.subheader('Overall sentiment score distribution')
        st.plotly_chart(fig)
    elif (selected_topic == "Society") & (selected_issue == "All"):
        st.subheader('Overall sentiment score distribution')
        st.plotly_chart(fig2)
    else:
        st.subheader(f'Sentiment score distribution in {selected_issue}')
        st.write(f'Top5 organizations')
        if selected_issue == "Sustainable development":
            st.plotly_chart(fig3)
        elif selected_issue == "climate change":
            st.plotly_chart(fig4)
        elif selected_issue == "marine ecology":
            st.plotly_chart(fig5)
        elif selected_issue == "carbon emission":
            st.plotly_chart(fig6)
        elif selected_issue == "human right":
            st.plotly_chart(fig7)
        elif selected_issue == "Racial discrimination":
            st.plotly_chart(fig8)
        elif selected_issue == "Social engagement":
            st.plotly_chart(fig9)
        elif selected_issue == "gap between rich and poor":
            st.plotly_chart(fig10)
        elif selected_issue == "Religious Conflicts":
            st.plotly_chart(fig11) 

    


    # S&P500 company
    st.subheader('Performance of S&P500 companies')
    # data    
    df_environment = pd.read_json('data/df_environment_ner.json')
    df_society = pd.read_json('data/df_society_ner.json')
    data_entities_pos_rate_environment = pd.read_json('data/data_entities_pos_rate_environment.json')
    data_entities_pos_rate_society = pd.read_json('data/data_entities_pos_rate_society.json')
    sp500 = pd.read_csv('data/constituents_csv.csv')
    sp500.loc[:, 'name_clean'] = [re.sub('\s((Brands\s)?Inc\.?|Company|Corp\.?|Bancorp|Technologies|\&?\s?Co\.|Entertainment|Corporation|Svc\.Gp\.)$', '', n) for n in sp500.Name]


    data_entities_pos_rate_environment.sort_values(by = 'sum', ascending = False, inplace = True, ignore_index= True)
    data_entities_pos_rate_society.sort_values(by = 'sum', ascending = False, inplace = True, ignore_index= True)

    # first topic choice
    if selected_topic == "Environment":
        entities_pos_rate = data_entities_pos_rate_environment.copy()
        topic_df = df_environment.copy()
    else:
        entities_pos_rate = data_entities_pos_rate_society.copy()
        topic_df = df_society.copy()

    # explode company_all
    topic_df['company'] = topic_df['company_all']
    topic_df_e = topic_df.explode('company')
    topic_df_e.reset_index(drop = True, inplace = True)
    # replace symbol/name by clean name
    for i in range(len(topic_df_e)):
        if topic_df_e.loc[i, 'company'] in sp500.Symbol.tolist():
            topic_df_e.loc[i, 'company'] = sp500.loc[sp500.Symbol == topic_df_e.loc[i, 'company'], 'name_clean'].values[0]
        elif topic_df_e.loc[i, 'company'] in sp500.Name.tolist():
            topic_df_e.loc[i, 'company'] = sp500.loc[sp500.Name == topic_df_e.loc[i, 'company'], 'name_clean'].values[0]
    topic_df_e.drop_duplicates(subset = ['head', 'company'], inplace=True, ignore_index=True)

    # overall:
    if selected_issue == 'All':  
        # calculate again
        entities_pos_rate_group = entities_pos_rate.groupby(by = 'entities').sum().reset_index()[['entities', '-1', '0', '1', 'sum']]
        entities_pos_rate_group['positive_rate'] = entities_pos_rate_group['1']/entities_pos_rate_group['sum']
        entities_pos_rate_group['neutral_rate'] = entities_pos_rate_group['0']/entities_pos_rate_group['sum']
        entities_pos_rate_group['negative_rate'] = entities_pos_rate_group['-1']/entities_pos_rate_group['sum']
        entities_pos_rate_group['score'] = ((entities_pos_rate_group['1']+(entities_pos_rate_group['0']*0.5))*100/entities_pos_rate_group['sum']).round(2)
        entities_pos_rate_group.sort_values(by = 'sum', ascending = False, inplace = True, ignore_index= True)
        # list top 5 company (by frequency)
        st.subheader('Top5 companies (by frequency)')
        st.markdown('Sort by number of news: ')
        topic_display = entities_pos_rate_group.rename(columns = {'entities': 'company', 'sum': 'total_news'})
        st.table(topic_display.loc[:5, ['company', 'total_news', 'score']])
        
        ### bubble plot ### 
        # only plot top5 company (by frequency)
        topic_top5_news = topic_df_e[topic_df_e.company.isin(topic_display.company.tolist()[:5])]
        topic_top5_news['time'] = pd.to_datetime(topic_top5_news['time'], format = '%Y-%m-%dT%H:%M:%SZ')  
        topic_top5_news['date'] = topic_top5_news['time'].dt.date
        # bubble plot: show the news' sentiment in timeline
        st.subheader('News distribution of top5 companies by the time')
        fig_topic_scatter = px.scatter(topic_top5_news, 
                                        x = 'date', y = 'nltk_compound',
                                        color = 'company', opacity=0.6, #size = 'sum', 
                                        hover_name = 'head', hover_data = ['source', 'category'],
                                        log_x = False, size_max = 50,
                                        color_discrete_sequence=px.colors.qualitative.T10)
        fig_topic_scatter.update_traces(marker_size = 12, opacity = 0.8)
        fig_topic_scatter.update_layout(autosize=False, width=800, height=400, 
                        margin=dict(l=5, r=5, b=5, t=5, pad=0),
                        showlegend=True
                        ) 
        st.plotly_chart(fig_topic_scatter)

        # box plot
        st.subheader('Sentiment score distribution of top5 companies')
        fig_topic_box = px.box(topic_top5_news,
                                x = 'company', y = 'nltk_compound',
                                color = 'company',
                                color_discrete_sequence=px.colors.qualitative.T10)
        fig_topic_box.update_layout(autosize=False, width=800, height=400, 
                        margin=dict(l=5, r=5, b=5, t=5, pad=0),
                        showlegend=True
                        ) 
        st.plotly_chart(fig_topic_box)


    # each issue:
    else:
        entities_pos_rate_issue = entities_pos_rate[entities_pos_rate.category == selected_issue]
        entities_pos_rate_issue['score'] = ((entities_pos_rate_issue['1']+(entities_pos_rate_issue['0']*0.5))*100/entities_pos_rate_issue['sum']).round(2)
        entities_pos_rate_issue.sort_values(by = 'sum', ascending=False, inplace=True, ignore_index=True)
        # list top 5 company (by frequency)
        st.markdown('Sort by number of news: ')
        issue_display = entities_pos_rate_issue.rename(columns = {'entities': 'company', 'sum': 'total_news'})
        st.table(issue_display.loc[:5, ['company', 'total_news', 'score']])
        
        ### bubble plot ### 
        # only plot top5 company (by frequency)
        issue_df = topic_df_e[topic_df_e.category == selected_issue]
        issue_top5_news = issue_df[issue_df.company.isin(issue_display.company.tolist()[:5])]
        issue_top5_news['time'] = pd.to_datetime(issue_top5_news['time'], format = '%Y-%m-%dT%H:%M:%SZ')  
        issue_top5_news['date'] = issue_top5_news['time'].dt.date
        # bubble plot: show the news' sentiment in timeline
        st.subheader('News distribution of top5 companies by the time')
        fig_issue_scatter = px.scatter(issue_top5_news, 
                                        x = 'date', y = 'nltk_compound',
                                        color = 'company', opacity=0.6, #size = 'sum', 
                                        hover_name = 'head', hover_data = ['source', 'category'],
                                        log_x = False, size_max = 50,
                                        color_discrete_sequence=px.colors.qualitative.T10)
        fig_issue_scatter.update_traces(marker_size = 12, opacity = 0.8)
        fig_issue_scatter.update_layout(autosize=False, width=800, height=400, 
                        margin=dict(l=5, r=5, b=5, t=5, pad=0),
                        showlegend=True
                        ) 
        st.plotly_chart(fig_issue_scatter)

        # box plot
        st.subheader('Sentiment score distribution of top5 companies')
        fig_issue_box = px.box(issue_top5_news,
                                x = 'company', y = 'nltk_compound',
                                color = 'company',
                                color_discrete_sequence=px.colors.qualitative.T10)
        fig_issue_box.update_layout(autosize=False, width=800, height=400, 
                        margin=dict(l=5, r=5, b=5, t=5, pad=0),
                        showlegend=True
                        ) 
        st.plotly_chart(fig_issue_box)