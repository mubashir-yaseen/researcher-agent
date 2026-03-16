from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Source(BaseModel):
    url: str
    title: str
    snippet: str
    credibility_score: float = Field(default=0.0)
    recency_score: float = Field(default=0.0)

class ResearchOutput(BaseModel):
    query: str
    timestamp: str = Field(default_factory=lambda: datetime.now().astimezone().isoformat())
    sources: List[Source]
    key_facts: List[str]
    confidence: float
    next_action: str
