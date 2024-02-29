import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

def get_html_content(url):
    """Fetches HTML content from the specified URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for error codes
    return response.content

def extract_news_articles(html_content, url):
    """Extracts news articles from the provided HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")

    news_articles = []
    if "moneycontrol" in url:
        for item in soup.find_all("li", class_="clearfix"):
            headline = item.find("h2").text.strip()
            article_url = item.find("a")["href"]
            image_url = item.find("img")["data-src"]
            content = item.find("p").text.strip()
            date = item.find("span").text.strip()
            news_articles.append({"headline": headline, "link": article_url, "image": image_url, "content": content, "date": date})
    else:
        for item in soup.find_all("div", class_="eachStory"):
            headline = item.find("h3").text.strip()
            article_url = item.find("a")["href"]
            image_url = item.find("img")["src"]
            date = item.find("time")["data-time"]
            content = item.find("p", class_="wrapLines").text.strip()
            news_articles.append({"headline": headline, "link": article_url, "image": image_url, "content": content, "date": date})

    return news_articles

def main():
    st.title("News Scraper App")
    
    website_choice = st.radio("Select a website to fetch news from:", ("Moneycontrol", "Economic Times"))

    if website_choice == "Moneycontrol":
        url = "https://www.moneycontrol.com/news/business/markets/"
    else:
        custom_url = "https://economictimes.indiatimes.com/news/economy/articlelist/1286551815.cms"
        url = custom_url

  

    while True:
        # Fetch HTML content and extract news articles
        html_content = get_html_content(url)
        news_articles = extract_news_articles(html_content, url)

        # Display news articles
        st.markdown("### Latest News Articles:")
        for article in news_articles:
            st.markdown(f"**{article['headline']}**")
            st.image(article['image'])
            st.markdown(f"*{article['content']}*")
            st.markdown(f"Published on: {article['date']}")
            st.markdown(f"[Read more]({article['link']})")
            st.markdown("---")
            
        # Refresh the data every hour
        time.sleep(3600)  # 3600 seconds = 1 hour

if __name__ == "__main__":
    main()
