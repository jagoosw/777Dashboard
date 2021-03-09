mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"jagoosw@protonmail.com\"">~/.streamlit/credentials.toml
echo “
[server]
headless = true
enableCORS=false
port = $PORT
“ > ~/.streamlit/config.toml
