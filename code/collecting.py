from .parsing import Parser, DromParser, DromPagingParser, DromScrollingParser
from .requesting import Requester, DromRequester
from .tools import CarType, Post
from .errors import NotSupportedCarType
from typing import Generator, Callable
import aiohttp

class PostCollector:
  parsers:dict[CarType, Parser]
  requester: Requester

  def __init__(self, session:aiohttp.ClientSession):
    self.requester = Requester(session)

  async def collect_posts(self, city:str, car_type:CarType) -> Generator[Post, None, None]:
    if car_type not in self.parsers:
      raise NotSupportedCarType
    async for url in await self.get_post_urls(city, car_type):
      yield self.parsers[car_type](await self.requester.get(url)).add_link(url)
  
  async def get_post_urls(self, city:str, car_type:CarType):
    raise NotImplementedError


class DromPostCollector(PostCollector):
  parsers: dict[CarType, DromParser]
  requester:DromRequester
  supported_car_types:set[CarType] = {CarType.AUTO, CarType.SPEC, CarType.MOTO}

  
  def __init__(self, session:aiohttp.ClientSession):
    p_parser = DromPagingParser()
    s_parser = DromScrollingParser()
    self.parsers = {
      CarType.AUTO: p_parser,
      CarType.SPEC: p_parser,
      CarType.MOTO: s_parser
    }
    self.requester = DromRequester(session)

  async def get_post_urls(self, city:str, car_type:CarType) -> Generator[str, None, None]:
    return self.__get_urls_by_pager(self.parsers[car_type], self.requester.get_pager(city, car_type))
    
  async def __get_urls_by_pager(self, parser:DromParser, get_page:Callable[[str, int], str]) -> Generator[str, None, None]: 
    for i in range(parser.get_page_count(await get_page(1))):
      list_page_content = await get_page(i+1)
      for url in parser.parse_list(list_page_content):
        yield url
