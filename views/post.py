from pydantic import BaseModel

from datetime import datetime

class PostOut(BaseModel):
    title: str
    date: datetime