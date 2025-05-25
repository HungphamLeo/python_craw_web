import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class ArticleScraper:
    def __init__(self, base_url, max_articles, max_days):
        self.base_url = base_url
        self.max_articles = max_articles
        self.max_days = timedelta(days=max_days)
        self.today = datetime.now()

    def scrape(self):
        articles, page = [], 1
        while len(articles) < self.max_articles:
            url = f"{self.base_url}/trang{page}.epi"
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.select("a[href*='.epi']"):
                article_url = self.base_url + a["href"]
                try:
                    article_resp = requests.get(article_url)
                    article_soup = BeautifulSoup(article_resp.text, "html.parser")
                    time_tag = article_soup.select_one("time")
                    if not time_tag:
                        continue
                    pub_time = datetime.strptime(time_tag.get("datetime"), "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
                    if self.today - pub_time <= self.max_days:
                        content = article_soup.get_text()
                        articles.append({"url": article_url, "content": content})
                except Exception:
                    continue
                if len(articles) >= self.max_articles:
                    break
            page += 1
        return articles
