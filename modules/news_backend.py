import streamlit as st
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from PIL import UnidentifiedImageError


news_api_key = st.secrets["NEWS_API_KEY"]

def get_news_api(search_news):
    date_today = datetime.today()
    a_month_ago = date_today - timedelta(days = 30)
    # Init
    newsapi = NewsApiClient(news_api_key)
    all_articles = newsapi.get_everything(q=f'{search_news}',
                                        sources='bbc-news,the-verge,bloomberg,hacker-news,wired,die-zeit,der-tagesspiegel',
                                        domains='bbc.co.uk,techcrunch.com,bloomberg.com,news.ycombinator.com,wired.com,zeit.de,tagesspiegel.de',
                                        from_param=a_month_ago,
                                        to=date_today,
                                        language='en',
                                        sort_by='relevancy',
                                        page=2)
    
    # debugger
    # st.write(all_articles["articles"][0])
    st.header(f"{len(all_articles['articles'])} results for: {search_news}")
    for i in range(len(all_articles['articles'])):
        try:
            st.header(all_articles['articles'][i]['title'])
            st.image(all_articles['articles'][i].get("urlToImage"))
            st.write(all_articles['articles'][i]['content'])
            article_author = all_articles['articles'][i]['author']
            if article_author is not None:
                st.write(f"by {article_author}")
            st.write(all_articles['articles'][i]['url'])      
        except IndexError:
            st.write('No results')
        except UnidentifiedImageError:
            st.error('Failed to display article.')
    

def view_sources():
    # /v2/top-headlines/sources
    newsapi = NewsApiClient(news_api_key)
    sources = newsapi.get_sources()
    st.header("SOURCES")
    st.table(sources["sources"])
