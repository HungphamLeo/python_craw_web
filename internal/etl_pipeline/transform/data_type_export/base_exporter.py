from abc import ABC, abstractmethod
from typing import List
from transform.data_type_export.dto import EntityDTO, ArticleDTO

class BaseExporter(ABC):
    
    @abstractmethod
    def export_entities(self, entities: List[EntityDTO], file_path: str) -> None:
        pass

    @abstractmethod
    def export_articles(self, articles: List[ArticleDTO], file_path: str) -> None:
        pass
