# schemas.py (Pydantic)
from pydantic import BaseModel

class SHabr(BaseModel):
    title: str
    author: str
    publish_date: str
    url: str