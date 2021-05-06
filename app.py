import streamlit as st
import app_overall_news
import app_keyword_search
import app_categories
import app_ppt
st.set_page_config(layout="wide")
# set the width of sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 200px;
        margin-left: -200px;
    }
    .stButton>button {
    height: 2em;
    width: 10em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
PAGES = {
    "Selected News": app_overall_news,
    "By Categories": app_categories,
    "Keyword Search": app_keyword_search,
    "PPT Generator": app_ppt
}
st.sidebar.title('Navigation')
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# page = PAGES[selection]
# page.app()
st.sidebar.markdown('\n')
PAGES_keys = list(PAGES.keys())
button_0 = st.sidebar.button(PAGES_keys[0])
button_1 = st.sidebar.button(PAGES_keys[1])
button_2 = st.sidebar.button(PAGES_keys[2])
button_3 = st.sidebar.button(PAGES_keys[3])

if button_0:
    PAGES[PAGES_keys[0]].app()
if button_1:
    PAGES[PAGES_keys[1]].app()
if button_2:
    PAGES[PAGES_keys[2]].app()
if button_3:
    PAGES[PAGES_keys[3]].app()
