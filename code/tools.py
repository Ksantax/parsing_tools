from enum import Enum
from dataclasses import dataclass
from typing import Self


@dataclass(init=True)
class Post:
  publishedAt:str
  price:str
  text:str
  properties:dict[str, str]
  source:str
  link:str = ''

  def add_link(self, url:str) -> Self:
    self.link = url
    return self
  
  def as_dict(self) -> dict[str, str | dict[str, str]]:
    return {
      "publishedAt": self.publishedAt,
      "price": self.price,
      "text": self.text,
      "properties": self.properties,
      "source": self.source,
      'link': self.link
    }


class CarType(Enum):
  AUTO = "auto"
  SPEC = "spec"
  MOTO = "moto"
