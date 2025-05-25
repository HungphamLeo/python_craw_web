import spacy
from collections import Counter

class NERModel:
    def __init__(self):
        self.model = spacy.load("vi_spacy_model")  # Replace with your Vietnamese model path

    def extract_entities(self, articles):
        entity_counter = Counter()
        for article in articles:
            doc = self.model(article["content"])
            for ent in doc.ents:
                entity_counter[ent.text] += 1
        return entity_counter.most_common(50)