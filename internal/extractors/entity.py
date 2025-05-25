# internal/models/ner_model.py
import spacy
from collections import Counter
from datetime import datetime
from internal.models.article_scraper_models import Entity
from global_file.global_file import global_config

class NERModel:
    def __init__(self):
        self.model = spacy.load("vi_spacy_model") 
        self.top_entity = global_config.config_loader.get_scraper_config()['top_entity']
        self.normalizer = EntityNormalizer()

    def extract_entities(self, articles):
        entity_counter = Counter()
        for article in articles:
            doc = self.model(article)
            for ent in doc.ents:
                entity_counter[ent.text] += 1
        return self.normalizer(entity_counter.most_common(self.top_entity))

class EntityNormalizer:
    def normalize(self, title: str, content: str, published_at: datetime) -> Entity:
        return Entity(id=None, title=title, content=content, published_at=published_at)
