from parsing import Parser, DromParser, DromPagingParser, DromScrollingParser
from requesting import Requester, DromRequester
from tools import CarType, Post
from errors import NotSupportedCarType
from typing import Generator, Callable
import aiohttp

class PostCollector:
  parser: Parser
  requester: Requester

  def __init__(self, session:aiohttp.ClientSession):
    self.requester = Requester(session)

  async def collect_posts(self, city:str, car_type:CarType) -> Generator[Post, None, None]:
    async for url in await self.get_post_urls(city, car_type):
      yield self.parser(await self.requester.get(url)).add_link(url)
  
  async def get_post_urls(self, city:str, car_type:CarType):
    raise NotImplementedError


class DromPostCollector(PostCollector):
  p_parser:DromPagingParser
  s_parser:DromPagingParser
  requester:DromRequester
  supported_car_types:set[CarType] = {CarType.AUTO, CarType.SPEC, CarType.MOTO}

  # Из-за разных дизайнов не получится сделать унифицированную реализацию
  # def __init__(self, *, parser:DromParser = None, requester:DromRequester = None):
  #   super().__init__(
  #     DromParser() if parser is None else parser, 
  #     DromRequester() if requester is None else reqFuester)
  def __init__(self, session:aiohttp.ClientSession):
    self.p_parser = DromPagingParser()
    self.s_parser = DromScrollingParser()
    self.requester = DromRequester(session)

  # И приходится переопределять основной метод класса
  async def collect_posts(self, city:str, car_type:CarType) -> Generator[Post, None, None]:
    async for url in await self.get_post_urls(city, car_type):
      post_text = await self.requester.get(url)
      if car_type is CarType.MOTO:
        yield self.s_parser(post_text).add_link(url)
      else:
        yield self.p_parser(post_text).add_link(url)

  async def get_post_urls(self, city:str, car_type:CarType) -> Generator[str, None, None]:
    if car_type in self.supported_car_types:
      if car_type is CarType.MOTO:
        return self.__get_urls_paging(self.s_parser, self.requester.get_pager(city, car_type))
      else:
        return self.__get_urls_paging(self.p_parser, self.requester.get_pager(city, car_type))
    else:
      raise NotSupportedCarType('Expected one of CarType values: '+\
        'CarType.Auto, CarType.SPEC, CarType.Moto. Given: '+str(car_type))

  async def __get_urls_paging(self, parser:DromParser, get_page:Callable[[str, int], str]) -> Generator[str, None, None]: 
    for i in range(parser.get_page_count(await get_page(1))):
      list_page_content = await get_page(i+1)
      for url in parser.parse_list(list_page_content):
        yield url
