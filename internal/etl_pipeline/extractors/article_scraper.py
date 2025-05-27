# internal/extractors/article_scraper.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from global_file.global_file import global_config
from internal.models.article_scraper_models import Article
from dateutil import parser
from transform.data_type_export.dto import EntityDTO
from transform.data_type_export.export_factory import ExportFactory



class ArticleNormalizer:
    def normalize(self, title: str, content: str, published_at: datetime) -> Article:
        
        return Article(id=None, title=title, content=content, published_at=published_at)

    def export_articles(self, articles: list[Article], file_path: None, export_status = False) -> None:
        if not export_status or not file_path:
            global_config.logger.info("Export status is False or file path is None. Skipping export.")
            return
        else:
            exporter = ExportFactory.get_exporter('excel')
            exporter.export_articles(articles, file_path)
            global_config.logger.info(f"Exported {len(articles)} articles to {file_path}")
            

class ArticleScraper:
    def __init__(self):
        self.max_articles = global_config.config_loader.get_scraper_config()['max_articles']
        self.base_url = global_config.config_loader.get_scraper_config()['url']
        self.articles = []
        self.visited_urls = set()
        self.today = datetime.now()
        self.max_days = timedelta(days=global_config.config_loader.get_scraper_config()['days'])
        self.normalizer = ArticleNormalizer()

    def scrape(self):
        page = 1
        while len(self.articles) < self.max_articles:
            url = f"{self.base_url}/trang{page}.epi"
            global_config.logger.info(f"Scraping page: {url}")
            try:
                resp = requests.get(url, timeout=5)
                soup = BeautifulSoup(resp.text, "html.parser")
            except Exception as e:
                global_config.logger.error(f"Error fetching page {page}: {e}")
                break

            article_links = soup.select("a[href*='.epi']")
            if not article_links:
                global_config.logger.info("No more articles found. Ending.")
                break

            for a in article_links:
                href = a.get("href")
                if not href or not href.endswith(".epi"):
                    continue

                article_url = self.base_url + href
                if article_url in self.visited_urls:
                    continue
                self.visited_urls.add(article_url)

                try:
                    article_resp = requests.get(article_url, timeout=5)
                    article_soup = BeautifulSoup(article_resp.text, "html.parser")

                    time_tag = article_soup.select_one("time")
                    if not time_tag or not time_tag.get("datetime"):
                        continue

                    pub_time = parser.isoparse(time_tag.get("datetime")).replace(tzinfo=None)
                    if self.today - pub_time > self.max_days:
                        continue

                    article_content = article_soup.get_text(separator=' ', strip=True)
                    article_title = article_soup.title.string if article_soup.title else "No Title"
                    article = self.normalizer.normalize(article_title, article_content, pub_time)
                    self.articles.append(article)
                    global_config.logger.info(f" Collected article {len(self.articles)} - {article_url}")

                except Exception as e:
                    global_config.logger.error(f"Error processing article: {e}")
                    continue

                if len(self.articles) >= self.max_articles:
                    break

            page += 1

        global_config.logger.info(f"\n Found {len(self.articles)} articles.")
        return self.articles
