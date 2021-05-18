import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
# import plotly.figure_factory as ff
# import altair as alt
# from PIL import Image

def app():

    # Sidebar
    st.subheader('KEYWORD SEARCH')

    # 多選按钮
    st.radio("Which would you choose", ['datetime', 'time','keyword'], key="3")

    

    col1,col2,col3,col4 = st.beta_columns(4)
    #search欄位
    with col1:
        def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
        selected = st.text_input("", "Search...")

    with col2:
        start_date = st.date_input("Start date", datetime.date(2019, 1, 1))
    
    with col3:
        end_date = st.date_input("End date", datetime.date(2021, 3, 1))

    #時間輸入
    with col4:
        time_input = st.time_input("Insert a time")

    

    #按紐
    st.button('GO')

    



    
