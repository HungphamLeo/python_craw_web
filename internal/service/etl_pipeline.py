# internal/pipelines/etl_pipeline.py
from internal.etl_pipeline.extractors.article_scraper import ArticleScraper
from internal.models.article_scraper_models import Entity
from internal.repo.mysql_repo import EntityRepositoryMySql, ArticleRepositoryMySQl
from internal.database.mysql.mysql_loaders import MySQLLoader
from internal.etl_pipeline.transform.entity import NERModel
from global_file.global_file import global_config


class ETLPipeline:
    def __init__(self):
        self.scraper = ArticleScraper()
        self.ner_model = NERModel()
        

        # Kiểm tra loại cơ sở dữ liệu từ cấu hình
        # db_type = global_config.config_loader.get_etl_config()['load']['destination']
        # if db_type == "mysql":
        #     self.loader = MySQLLoader()
        #     self.entity_repository = EntityRepositoryMySql(self.loader)
        #     self.article_repository = ArticleRepositoryMySQl(self.loader)
        # else:
        #     raise ValueError(f"Unsupported database type: {db_type}")

    def run(self):
        try:
            articles = self.scraper.scrape()
            entities = self.ner_model.extract_entities(articles)
            for entity in entities:
            #     self.entity_repository.save(entity)
            # self.loader.close()
                global_config.logger.info(f'----------------------- Here is entity ------------')
                global_config.logger.info(f'entity: {entity}')
        except Exception as e:
            global_config.logger.error(f"ETL Pipeline failed: {e}")
            raise e