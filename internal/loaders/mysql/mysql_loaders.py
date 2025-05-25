# internal/loaders/mysql_loader.py
import mysql.connector
from mysql.connector import Error
from global_file.global_file import global_config

class MySQLLoader:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Initialize MySQL connection."""
        try:
            config = global_config.config_loader.get_mysql_config()
            self.conn = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            self.cursor = self.conn.cursor()
            global_config.logger.info("Connected to MySQL database successfully")
            self.set_pool()
        except Error as e:
            global_config.logger.error(f"Error connecting to MySQL: {e}")
            raise

    def set_pool(self):
        """Set connection pool parameters."""
        if self.conn:
            self.conn.pool_size = global_config.config_loader.get_mysql_config()['pool_size']
            global_config.logger.info("Connection pool set successfully")

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            global_config.logger.info("MySQL connection closed")

    def check_health(self):
        """Check the health of the database connection."""
        try:
            if self.conn.is_connected():
                global_config.logger.info("MySQL connection is healthy")
                return True
            else:
                global_config.logger.error("MySQL connection is not healthy")
                return False
        except Error as e:
            global_config.logger.error(f"Error checking MySQL connection: {e}")
            return False
