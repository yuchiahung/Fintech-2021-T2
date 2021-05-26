import pandas as pd
import numpy as np
import streamlit as st

def app():
    st.title('ESG Media Trend')
    search = st.beta_expander('Search', False)
    col1,col2 = search.beta_columns(2)
    #search
    with col1:
        company = st.text_input("Search a company", "Search...")
    with col2:
        options = ['Environment',' Social']
        topic = st.multiselect('Select topics:', options, options)
    if (company == 'Search...') and (len(topic) == 0):
        st.write('Please select a company and topics')
    elif (company == 'Search...') and (len(topic) != 0):
        st.write('Please select a company')
    elif (company != 'Search...') and (len(topic) == 0):
        st.write('Please select topics')

    page_dashboard(company, topic)


def page_dashboard(company, topic):
    if company != 'Search...':
        st.header(company.upper())
    df = pd.read_json('test_summary_data.json')

    #select company
    display_df = df.loc[df.content_summary.str.contains(company)]

    #select topic
    topic_1 = topic[0]
    if len(topic) == 2:
        topic_2 = topic[1]
        col3,col4 = st.beta_columns(2)
        with col3:
            st.header(topic[0].upper())
            display_df_1 = display_df.loc[df.category == topic_1]
        with col4:
            st.header(topic[1].upper())
            display_df_2 = display_df.loc[df.category == topic_2]
    elif len(topic) == 1:
        st.header(topic[0].upper())
        display_df_1 = display_df.loc[df.category == topic_1]