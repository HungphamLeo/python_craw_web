import yaml
import logging

class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get_logger_config(self):
        return self.config['logger']

    def get_mysql_config(self):
        return self.config['mysql']

    def get_hdfs_config(self):
        return self.config['hdfs']

    def get_docker_config(self):
        return self.config['docker']

    def get_spark_config(self):
        return self.config['spark']

    def get_redis_config(self):
        return self.config['redis']

    def get_kafka_config(self):
        return self.config['kafka']

    def get_scraper_config(self):
        return self.config['scraper']

    def get_etl_config(self):
        return self.config['etl']

# # Usage
# if __name__ == "__main__":
#     config_loader = ConfigLoader('config/config.yaml')
#     logger_config = config_loader.get_logger_config()
#     logging.basicConfig(level=logger_config['level'], format=logger_config['format'], filename=logger_config['file'])
#     logging.info("Logger is configured.")
