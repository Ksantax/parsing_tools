from typing import NamedTuple
from pathlib import Path
from .tools import CarType
from .parsing import Parser


link = str


class PagingCfg(NamedTuple):
  source:str
  cities_file_path:Path
  parsers_links:dict[CarType, tuple[Parser, link]]
  delay_interval:tuple[int] = None
  headers:dict[str, str] = None

  @property
  def links(self) -> dict[CarType, link]:
    return {car_type: link_ for car_type, (_, link_) in self.parsers_links.items()}
  
  @property
  def parsers(self) -> dict[CarType, Parser]:
    return {car_type: parser for car_type, (parser, _) in self.parsers_links.items()}
