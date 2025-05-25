# internal/pipelines/etl_pipeline.py
from internal.extractors.article_scraper import ArticleScraper
from internal.models.article_scraper_models import Entity
from internal.repo.mysql_repo import EntityRepository
from internal.loaders.mysql.mysql_loaders import MySQLLoader
from internal.extractors.entity import NERModel
class ETLPipeline:
    def __init__(self):
        self.scraper = ArticleScraper()
        self.ner_model = NERModel()
        self.loader = MySQLLoader()
        self.repository = EntityRepository(self.loader)

    def run(self):
        articles = self.scraper.scrape()  # Bước Extract
        entities = self.ner_model.extract_entities(articles)
        for entity in entities:
            self.repository.save(Entity(id=None, text=entity[0], count=entity[1]))  # Bước Load
        self.loader.close()
