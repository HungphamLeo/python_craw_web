# Removed unused: import spacy
from collections import Counter
from datetime import datetime
from internal.models.article_scraper_models import Entity # Assuming this path is correct
from global_file.global_file import global_config # Assuming this path is correct
from pyvi import ViTokenizer, ViPosTagger
from transform.data_type_export.dto import EntityDTO
from transform.data_type_export.export_factory import ExportFactory

class NERModel:
    def __init__(self):
        scraper_config = global_config.config_loader.get_scraper_config()
        # Provide a default for top_entity if not found in config to prevent KeyError
        self.top_entity = scraper_config.get('top_entity', 10) # Default to 10 if not specified
        self.normalizer = EntityNormalizer()
        # It's good practice to ensure logger is available
        self.logger = global_config.logger if hasattr(global_config, 'logger') else print # Fallback to print if logger not set

    def extract_entities(self, articles):
        entity_counter = Counter()

        for article_idx, article in enumerate(articles):
            # Basic check for article content
            if not hasattr(article, 'content') or not isinstance(article.content, str) or not article.content.strip():
                self.logger.warning(f"Article {article_idx} has missing, invalid, or empty content. Skipping.")
                continue

            tokenized_text = ViTokenizer.tokenize(article.content)
            # self.logger.info(f"Tokenized text for article {article_idx}: {tokenized_text}") # Original logging

            # ViPosTagger.postagging expects a string of space-separated tokens (which ViTokenizer.tokenize provides)
            words, pos_tags = ViPosTagger.postagging(tokenized_text)

            # self.logger.info(f"Words: {words}, POS Tags: {pos_tags}") # For debugging

            current_chunk = []
            for i in range(len(words)):
                word = words[i].replace("_", " ") # Replace underscores with spaces for readability
                pos = pos_tags[i]

                if pos == "Np": # Proper noun
                    current_chunk.append(word)
                else:
                    if current_chunk:
                        # Join collected proper nouns to form a multi-word entity
                        entity_name = " ".join(current_chunk)
                        entity_counter[entity_name] += 1
                        current_chunk = []
            
            # After the loop, add any remaining entity in current_chunk
            if current_chunk:
                entity_name = " ".join(current_chunk)
                entity_counter[entity_name] += 1
        
        # Get the most common entities based on the chunked names
        most_common_raw_entities = entity_counter.most_common(self.top_entity)
        # self.logger.info(f"Most common raw entities: {most_common_raw_entities}") # For debugging
        
        return self.normalizer(most_common_raw_entities)


class EntityNormalizer:
    def __init__(self):
        self.scraper_config = global_config.config_loader.get_scraper_config()
        self.export_status = self.scraper_config.get('export_entity_status', False)
        self.file_path = self.scraper_config.get('export_entity_path')

    def __call__(self, most_common_entities):
        entity_list = [
            Entity(id=None, text=name.strip(), frequency=str(count), published_at=None)
            for name, count in most_common_entities
        ]

        if self.export_status and self.file_path:
            self.export_entities(entity_list)

        return entity_list


    def export_entities(self, entities):
        exporter = ExportFactory.get_exporter('excel')
        exporter.export_entities(entities, self.file_path)

