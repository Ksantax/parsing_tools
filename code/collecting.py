from parsing import Parser, DromParser
from requesting import Requester, DromRequester
from tools import CarType, Post
from errors import NotSupportedCarType
from typing import Generator, Callable

class PostCollector:
  parser: Parser
  requester: Requester

  def __init__(self, parser:Parser, requester:Requester):
    self.parser = parser
    self.requester = requester

  async def collect_posts(self, city:str, car_type:CarType) -> list[Post]:
    return [self.parser(await self.requester.get(url)).add_link(url)
            for url in self.get_post_urls(city, car_type)]
  
  async def get_post_urls(self, city:str, car_type:CarType):
    raise NotImplementedError("PostCollector -- is abstract class.")


class DromPostCollector(PostCollector):
  parser: DromParser
  requester: DromRequester
  supported_car_types:set[CarType] = {CarType.AUTO, CarType.SPEC, CarType.MOTO}

  def __init__(self, *, parser:DromParser = None, requester:DromRequester = None):
    super().__init__(
      DromParser() if parser is None else parser, 
      DromRequester() if requester is None else requester)

  async def get_post_urls(self, city:str, car_type:CarType) -> Generator[str, None, None]:
    if car_type in self.supported_car_types:
      return self.__get_urls_paging(car_type, self.requester.get_pager(city))
    else:
      raise NotSupportedCarType('Expected one of CarType values: '+\
        'CarType.Auto, CarType.SPEC, CarType.Moto. Given: '+str(car_type))

  async def __get_urls_paging(self, car_type:CarType, get_page:Callable[[str, int], str]) -> Generator[str, None, None]: 
    async for i in range(self.parser.get_page_count(car_type, await get_page(1))):
      list_page_content = await get_page(i+1)
      for url in self.parser.parse_list(car_type, list_page_content):
        yield url
  





