from tech_news.database import search_news
from tech_news.database import find_news
from datetime import datetime
from typing import Dict, List


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    return [(news["title"], news["url"]) for news in search_news(query)]


# Requisito 8
def search_by_date(date: str) -> List[Dict[str, str]]:
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
    except ValueError:
        raise ValueError("Data inválida")

    result = []
    for new in find_news():
        if new["timestamp"] == formatted_date:
            result.append(new)
    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
