from config.loader import load_config
from internal.extractors.article_scraper import ArticleScraper
from internal.transform.ner import NERModel
from internal.loaders.mysql.loader import MySQLLoader
from global.global import logger

class BaomoiETLPipeline:
    def __init__(self):
        self.config = load_config()

    def run(self):
        logger.info("Starting ETL pipeline")

        scraper = ArticleScraper(
            base_url=self.config["scraper"]["base_url"],
            max_articles=self.config["scraper"]["max_articles"],
            max_days=self.config["scraper"]["days_range"]
        )
        articles = scraper.scrape()

        logger.info(f"Scraped {len(articles)} articles")

        ner = NERModel()
        top_entities = ner.extract_entities(articles)

        logger.info(f"Extracted top {len(top_entities)} entities")

        loader = MySQLLoader(host="localhost", user="root", password="", database="baomoi")
        loader.insert_entities(top_entities)
        loader.close()

        logger.info("ETL pipeline completed successfully")
