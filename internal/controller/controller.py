# internal/controllers/etl_controller.py
from internal.service.etl_pipeline import ETLPipeline
from global_file.global_file    import global_config

class ETLController:
    def __init__(self):
        self.pipeline = ETLPipeline()
        # class object any services.

    def run(self):
        global_config.logger.info("Running ETL process...")
        self.pipeline.run()
        global_config.logger.info("ETL process completed.")
