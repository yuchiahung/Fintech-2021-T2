from typing import KeysView
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import json



def app():
    st.title('ESG Media Trend')
    search = st.beta_expander('Search', False)
    col1,col2 = search.beta_columns(2)
    
    with col1:
        options = ["Sentiment of title", "Issue"]
        option = ["Environment","Society"]
        option_2 = ["Sustainable development","climate change","marine ecology","carbon emission","human right","Racial discrimination","Social engagement","gap between rich and poor","Religious Conflicts"]
        page = st.selectbox("please select an option", options=options)
    
    with col2:
        if page == "Sentiment of title":
            selection = st.selectbox("please select a topic", option)
        if page == "Issue":
            selection = st.selectbox("please select an issue", option_2)

    
    
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
    st.plotly_chart(fig)

    fig2 = px.box(df_2,
                    x = 'category', y = 'nltk_compound',
                    color = 'category',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig2)

    fig3 = px.box(df10,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig3)

    fig4 = px.box(df18,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig4)

    fig5 = px.box(df26,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig5)

    fig6 = px.box(df34,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig6)

    fig7 = px.box(df42,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig7)

    fig8 = px.box(df50,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig8)

    fig9 = px.box(df58,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig9)

    fig10 = px.box(df66,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig10)

    fig11 = px.box(df74,
                    x = 'organize_name', y = 'nltk_compound',
                    color = 'organize_name',
                    color_discrete_sequence=px.colors.qualitative.T10)
    fig2.update_layout(autosize=False, width=800, height=400, 
                    margin=dict(l=5, r=5, b=5, t=5, pad=0),
                    showlegend=True
                    ) 
    st.plotly_chart(fig11)

    


    

    
    


        
