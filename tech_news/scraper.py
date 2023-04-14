import requests
import time
from parsel import Selector
from bs4 import BeautifulSoup
from tech_news.database import create_news


def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    links = selector.css(".entry-title a::attr(href)").getall()
    return links


# Requisito 3
# https://app.betrybe.com/learn/course/5e938f69-6e32-43b3-9685-c936530fd326/module/290e715d-73e3-4b2d-a3c7-4fe113474070/section/7e82ac53-a588-412b-95a5-19727d70ed3a/day/a830c6e2-bcb7-4124-a230-453a8cd952bf/lesson/ba10411c-a220-4589-98af-6653fe9bd525
def scrape_next_page_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    next_page_link = soup.find("a", class_="next page-numbers")
    if next_page_link:
        return next_page_link["href"]
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)

    return {
        "url": selector.css("link[rel='canonical']::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css("span.author a::text").get(),
        "reading_time": int(
            selector.css("li.meta-reading-time::text").re_first(r"\d+")
        ),
        "summary": "".join(
            selector.css(".entry-content > p:first-of-type *::text").getall()
        ).strip(),
        "category": selector.css("div.meta-category span.label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    page = fetch("https://blog.betrybe.com/")
    next_link = scrape_next_page_link(page)
    links = scrape_updates(page)

    while len(links) < amount:
        next_page = fetch(next_link)
        links.extend(scrape_updates(next_page))
        next_link = scrape_next_page_link(next_page)
    news = [scrape_news(fetch(link)) for link in links[:amount]]
    create_news(news)
    return news
