# internal/models/article.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    id: int
    title: str
    content: str
    published_at: datetime

@dataclass
class Entity:
    id: int
    text: str
    frequency: str
    published_at: datetime
