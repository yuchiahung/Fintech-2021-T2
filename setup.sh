mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"a10230911@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]
primaryColor='#9C9E98'
backgroundColor='#f5faff'
secondaryBackgroundColor='#d1e2eb'
textColor='#262730'
font='sans serif'
" > ~/.streamlit/config.toml