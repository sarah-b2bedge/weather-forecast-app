import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")

topic = "finance"

st.title("News Summarizer")
st.subheader(topic.upper())

url = ("https://newsapi.org/v2/everything?"
       f"q={topic}&"
       "sortBy=publishedAt&"
       f"apiKey={news_api_key}&"
       "language=en")

# Make request
request = requests.get(url)

# Get a dictionary with the response data
content = request.json()

# Access the article titles and descriptions
body = "<br>"
for article in content["articles"][0:20]:
    if article["title"] is not None and article["description"] is not None:
        body = body + f'<b>{article["title"]}</b>' + "<br>" \
                + article["description"] + "<br>" \
                + f'<a href="{article["url"]}">Read more</a><br><br>'

st.text("")
st.write(body, unsafe_allow_html=True)