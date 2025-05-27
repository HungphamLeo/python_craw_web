from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EntityDTO:
    text: str
    count: int

@dataclass
class ArticleDTO:
    title: str
    published_at: Optional[datetime]
    content: str
