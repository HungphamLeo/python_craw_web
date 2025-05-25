from config.loader import ConfigLoader

class GlobalConfig:
    def __init__(self):
        self.config_loader = ConfigLoader('config/config.yaml')
        self.mysql_config = self.config_loader.get_mysql_config()
        self.hdfs_config = self.config_loader.get_hdfs_config()
        self.docker_config = self.config_loader.get_docker_config()
        self.spark_config = self.config_loader.get_spark_config()
        self.redis_config = self.config_loader.get_redis_config()
        self.kafka_config = self.config_loader.get_kafka_config()
        self.scraper_config = self.config_loader.get_scraper_config()
        self.etl_config = self.config_loader.get_etl_config()


