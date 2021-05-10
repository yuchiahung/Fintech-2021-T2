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
    st.sidebar.subheader('KEYWORD SEARCH')

    # 多選按钮
    st.sidebar.radio("Which would you choose", ['datetime', 'time','keyword'], key="3")

    # 單選選框
    selector = st.sidebar.multiselect("Which would you choose", ['datetime', 'time','keyword'], key="1")
    st.write(selector)

    start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 3, 1))

    #時間輸入
    time_input = st.sidebar.time_input("Insert a time")

    #search欄位
    def icon(icon_name):
        st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
    selected = st.sidebar.text_input("", "Search...")

    #按紐
    button_go = st.sidebar.button('GO')
    if button_go:
        st.write(start_date)



    