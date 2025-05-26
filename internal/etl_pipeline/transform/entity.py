# Removed unused: import spacy
from collections import Counter
# Assuming datetime might be used by Entity or other parts, kept for now.
# If Entity doesn't use published_at from a datetime object here, it could be removed
# if not used elsewhere. For now, let's assume Entity might need it or it was a placeholder.
from datetime import datetime
from internal.models.article_scraper_models import Entity # Assuming this path is correct
from global_file.global_file import global_config # Assuming this path is correct
from pyvi import ViTokenizer, ViPosTagger

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
    def __call__(self, most_common_entities):
        # most_common_entities is a list of (entity_name, count) tuples
        # The Entity model expects: id, title, content, published_at
        # We are setting title to the extracted entity_name.
        # Other fields are defaults as per the original code.
        return [Entity(id=None, text=ent[0], content="", published_at=None) for ent in most_common_entities]