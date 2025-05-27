import pandas as pd
from typing import List
from transform.data_type_export.base_exporter import BaseExporter
from transform.data_type_export.dto import EntityDTO, ArticleDTO

class ExcelExporter(BaseExporter):

    def export_entities(self, entities: List[EntityDTO], file_path: str) -> None:
        df = pd.DataFrame([e.__dict__ for e in entities])
        df.to_excel(file_path, index=False)

    def export_articles(self, articles: List[ArticleDTO], file_path: str) -> None:
        df = pd.DataFrame([a.__dict__ for a in articles])
        df.to_excel(file_path, index=False)
