import bs4
from tools import CarType


class Parser:
  # TODO: Make returning a Post class object, not a dict
  def parse_post(post_page_text:str) -> dict:
    raise NotImplementedError
  

  def __call__(self, post_page_text:str) -> dict:
    return self.parse_post(post_page_text)


class DromParser(Parser):
  def __init__(self):
    pass

  def parse_post(self, post_page_text:str) -> dict:
    pass

  def parse_list(self) -> list:
    pass

