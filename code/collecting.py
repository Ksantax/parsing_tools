from parsing import Parser, DromParser, DromPagingParser, DromScrollingParser
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
    raise NotImplementedError


class DromPostCollector(PostCollector):
  p_parser:DromPagingParser = DromPagingParser()
  s_parser:DromPagingParser = DromScrollingParser()
  requester:DromRequester = DromRequester()
  supported_car_types:set[CarType] = {CarType.AUTO, CarType.SPEC, CarType.MOTO}

  # Из-за разных дизайнов не получится сделать унифицированную реализацию
  # def __init__(self, *, parser:DromParser = None, requester:DromRequester = None):
  #   super().__init__(
  #     DromParser() if parser is None else parser, 
  #     DromRequester() if requester is None else requester)

  # И приходится переопределять основной метод класса
  async def collect_posts(self, city:str, car_type:CarType) -> list[Post]:
    res = []
    async for url in await self.get_post_urls(city, car_type):
      post_text = await self.requester.get(url)
      if car_type is CarType.MOTO:
        res.append(self.s_parser(post_text))
      else:
        res.append(self.p_parser(post_text))
    return res

  async def get_post_urls(self, city:str, car_type:CarType) -> Generator[str, None, None]:
    if car_type in self.supported_car_types:
      if car_type is CarType.MOTO:
        return self.__get_urls_paging(self.s_parser, self.requester.get_pager(city))
      else:
        return self.__get_urls_paging(self.p_parser, self.requester.get_pager(city))
    else:
      raise NotSupportedCarType('Expected one of CarType values: '+\
        'CarType.Auto, CarType.SPEC, CarType.Moto. Given: '+str(car_type))

  async def __get_urls_paging(self, parser:DromParser, get_page:Callable[[str, int], str]) -> Generator[str, None, None]: 
    async for i in range(parser.get_page_count(await get_page(1))):
      list_page_content = await get_page(i+1)
      for url in parser.parse_list(list_page_content):
        yield url
