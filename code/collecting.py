from .parsing import Parser, DromParser, DromPagingParser, DromScrollingParser
from .requesting import Requester, DromRequester
from collections import defaultdict
from .tools import CarType, Post
from .errors import NotSupportedCarType
from typing import AsyncGenerator, Callable, Iterable
import aiohttp
from pathlib import Path
import os


MODULE_DIR = os.path.dirname(__file__) + '\\'
CACHE_DIR = MODULE_DIR+'cache\\drom\\'


class PostCollector:
  parsers:dict[CarType, Parser]
  requester: Requester

  def __init__(self, session:aiohttp.ClientSession):
    self.requester = Requester(session)

  async def collect_posts(self, city:str, car_type:CarType) -> AsyncGenerator[Post, None]:
    if car_type not in self.parsers:
      raise NotSupportedCarType
    urls = [url async for url in self.get_post_urls(city, car_type)]
    for url in self.reduce_urls(urls, city, car_type):
      yield self.parsers[car_type](await self.requester.get(url)).add_link(url)
  
  def reduce_urls(self, urls:Iterable[str], city:str, car_type:CarType) -> Iterable[str]:
    cache_file = Path(CACHE_DIR+f'{city}\\{car_type.value}.txt')
    cache_file.parent.mkdir(exist_ok=True, parents=True)
    old_urlrs = cache_file.read_text().splitlines()
    cache_file.write_text('\n'.join(urls))
    return set(urls) - set(old_urlrs)

  async def get_post_urls(self, city:str, car_type:CarType) -> AsyncGenerator[str, None]:
    raise NotImplementedError


class DromPostCollector(PostCollector):
  parsers: dict[CarType, DromParser]
  requester:DromRequester
  supported_car_types:set[CarType] = {CarType.AUTO, CarType.SPEC, CarType.MOTO}
  __cache:defaultdict[str, dict[CarType, str]] = defaultdict(lambda: {
    CarType.AUTO: '',
    CarType.SPEC: '',
    CarType.MOTO: ''
  })

  
  def __init__(self, session:aiohttp.ClientSession):
    p_parser = DromPagingParser()
    s_parser = DromScrollingParser()
    self.parsers = {
      CarType.AUTO: p_parser,
      CarType.SPEC: p_parser,
      CarType.MOTO: s_parser
    }
    self.requester = DromRequester(session)

  async def get_post_urls(self, city:str, car_type:CarType) -> AsyncGenerator[str, None]:
    get_page:Callable[[int], str] = self.requester.get_pager(city, car_type)    
    for i in range(self.parsers[car_type].get_page_count(await get_page(1))):
      list_page_content = await get_page(i+1)
      for url in self.parsers[car_type].parse_list(list_page_content):
        yield url
  
  def reduce_urls(self, urls: Iterable[str], city: str, car_type: CarType) -> Iterable[str]:
    res = list()
    for url in urls:
      if url == self.__cache[city][car_type]:
        break
      res.append(url)
    self.__cache[city][car_type] = next(iter(urls))
    return res
