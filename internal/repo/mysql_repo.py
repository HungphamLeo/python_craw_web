# internal/repos/mysql_repository.py
from internal.loaders.mysql.mysql_loaders import MySQLLoader
from internal.models.article_scraper_models import Article
from internal.models.article_scraper_models import Entity
from global_file.global_file import global_config
class ArticleRepository:
    def __init__(self, loader: MySQLLoader):
        self.loader = loader

    def create_table(self):
        """Create the articles table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            published_at DATETIME NOT NULL
        )
        """
        self.loader.cursor.execute(create_table_query)
        self.loader.conn.commit()
        global_config.logger.info("Articles table created successfully")

    def save(self, article: Article):
        """Insert an article into the database."""
        query = "INSERT INTO articles (title, content, published_at) VALUES (%s, %s, %s)"
        self.loader.cursor.execute(query, (article.title, article.content, article.published_at))
        self.loader.conn.commit()
        global_config.logger.info(f"Article '{article.title}' saved successfully")

    def get_all(self):
        """Retrieve all articles from the database."""
        query = "SELECT * FROM articles"
        self.loader.cursor.execute(query)
        return self.loader.cursor.fetchall()


class EntityRepository:
    def __init__(self, loader: MySQLLoader):
        self.loader = loader
    def save(self, entity: Entity):
        query = "INSERT INTO entities (id, text, count) VALUES (%s, %s, %s)"
        self.loader.cursor.execute(query, (entity.id, entity.text, entity.count))
        self.loader.conn.commit()
    def get_all(self):
        query = "SELECT * FROM entities"
        self.loader.cursor.execute(query)
        return self.loader.cursor.fetchall()

# Class khác
#......
# Các phương thức khác để tương tác với cơ sở dữ liệu của các service khác có thể được thêm vào đây