from post_parsers import *
from tools import CarType
from errors import *
import async_requests as req



class PostCollector:
  async def collect_posts(self, city:str, car_type:CarType) -> list:
    raise NotImplementedError



class DromPostCollector(PostCollector):
  car_type_urls = {
    CarType.AUTO: ['https://{}.drom.ru/auto/all/page{}/?unsold=1'],
    CarType.SPEC: ['https://{}.drom.ru/spec/all/page{}/?unsold=1']
  }
  parser:DromParser

  def __init__(self, parser:DromParser=None):
    self.parser = parser if parser else DromParser()
  
  async def collect_posts(self, city: str, car_type: CarType) -> list:
    if CarType is CarType.MOTO:
      raise NotSupportedCarType(
        'MOTO car type is not supported by DromPostCollector, '+\
        'use DromMotoPostCollector instead')
    return [self.parser(await req.get(url)) for url in self.__get_uls(city, car_type)]
  

  async def __get_uls(self, city, car_type):
    pass


class DromMotoPostCollector(DromPostCollector):
  pass



# TODO: add title collecting