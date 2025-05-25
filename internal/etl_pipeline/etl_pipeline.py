# internal/pipelines/etl_pipeline.py
from internal.extractors.article_scraper import ArticleScraper
from internal.models.ner_model import NERModel
from internal.loaders.mysql_loader import MySQLLoader
from global_file.global_file import global_config

class ETLPipeline:
    def __init__(self):
        self.scraper = ArticleScraper()
        self.ner_model = NERModel()
        self.loader = MySQLLoader(
            host=global_config.config_loader.get_mysql_config()['host'],
            user=global_config.config_loader.get_mysql_config()['user'],
            password=global_config.config_loader.get_mysql_config()['password'],
            database=global_config.config_loader.get_mysql_config()['database']
        )

    def run(self):
        global_config.logger.info("Starting ETL pipeline")

        articles = self.scraper.scrape()  # Bước Extract
        global_config.logger.info(f"Scraped {len(articles)} articles")

        top_entities = self.ner_model.extract_entities(articles)  # Bước Transform
        global_config.logger.info(f"Extracted top {len(top_entities)} entities")

        self.loader.insert_entities(top_entities)  # Bước Load
        self.loader.close()

        global_config.logger.info("ETL pipeline completed successfully")
