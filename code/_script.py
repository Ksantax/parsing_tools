from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
  publishedAt: datetime
  text: str
  city: str
  url: str
  source: str

  def __init__(self, 
  publishedAt: datetime,
  text: str,
  city: str,
  url: str,
  source: str):
    super().__init__(publishedAt=publishedAt, text=text, 
                      city=city, url=url, source=source)
