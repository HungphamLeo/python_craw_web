import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config.loader import ConfigLoader

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        """
        Implement Singleton pattern for the given class.

        This method is automatically called when an instance of the class is
        created. If the class is not yet in the `_instances` dictionary, it
        creates a new instance and store it in the dictionary. If the class is
        already in the dictionary, it simply returns the existing instance.

        :param args: The arguments to be passed to the constructor of the class.
        :param kwargs: The keyword arguments to be passed to the constructor of
            the class.
        :return: The instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerManager(metaclass=SingletonMeta):
    def __init__(self):
        """
        Initialize the logger with the configuration from the config file.

        :param config_file: The path to the configuration file.
        """
        config_loader = ConfigLoader('config/config.yaml')
        logger_config = config_loader.get_logger_config()

        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logger_config['level'])
        self.logger.propagate = False

        log_path = Path(logger_config['storage_path'])
        log_path.mkdir(parents=True, exist_ok=True)

        # Tạo các file log cho từng mức độ
        log_files = {
            logging.DEBUG: logger_config['files']['debug'],
            logging.INFO: logger_config['files']['info'],
            logging.WARNING: logger_config['files']['warning'],
            logging.ERROR: logger_config['files']['error'],
        }

        formatter = logging.Formatter(
            fmt='{"time":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s", "caller":"%(pathname)s:%(lineno)d"}',
            datefmt="%Y-%m-%dT%H:%M:%S"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Thêm các file handler cho từng mức độ log
        for level, log_file in log_files.items():
            log_full_path = log_path / log_file
            file_handler = RotatingFileHandler(
                filename=log_full_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=3
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Thêm console handler
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
