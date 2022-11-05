from post_parsers import *
from tools import CarType



class PostCollector:
  def __init__(self, city:str, car_type:CarType):
    self.city = city
    self.

  def collect_posts(self) -> list:
    raise NotImplementedError


class DromPostCollector(PostCollector):
  parser:DromPostParser

  def __init__(self, )