from .parsing import Parser, DromParser
from .requesting import Requester, PagingRequester
from .tools import CarType, Post
from .errors import NotSupportedCarType
from .configurating import PagingCfg
from typing import AsyncGenerator, Callable, Iterable
from pathlib import Path
import json, asyncio, random
from .config import CACHE_DIR, POST_LIMIT


def create_file_if_not_exists(file_path:Path, encoding='utf-8') -> None:
  if not file_path.exists():
    file_path.parent.mkdir(exist_ok=True, parents=True)
    with open(file_path, 'w+', encoding=encoding) as file:
      file.write('')


class PostCollector:
  parsers:dict[CarType, Parser]
  requester: Requester
  cities:dict[str, str]
  cache_file_name: str
  delay_interval:tuple[float] = None

  async def collect_posts(self, city:str, car_type:CarType) -> AsyncGenerator[Post, None]:
    if city not in self.cities:
      return 
    city = self.cities[city]
    if car_type not in self.parsers:
      raise NotSupportedCarType(f'Not supported {car_type} for {type(self)} collector')
    urls = [url async for url in self.get_post_urls(city, car_type)]
    for url in self.reduce_urls(urls, city, car_type):
      if self.delay_interval:
        await asyncio.sleep(random.uniform(*self.delay_interval))
      yield self.parsers[car_type](await self.requester.get(url)).add_link(url)
  
  def reduce_urls(self, urls:Iterable[str], city:str, car_type:CarType) -> Iterable[str]:
    cache_file:Path = CACHE_DIR / city / car_type.value / self.cache_file_name
    create_file_if_not_exists(cache_file)
    old_urlrs = cache_file.read_text(encoding='utf-8').splitlines()
    cache_file.write_text('\n'.join(urls), encoding='utf-8')
    return set(urls) - set(old_urlrs)

  def supports(self, car_type:CarType) -> bool:
    raise NotImplementedError

  async def get_post_urls(self, city:str, car_type:CarType) -> AsyncGenerator[str, None]:
    raise NotImplementedError


class PagingPostCollector(PostCollector):
  parsers: dict[CarType, DromParser]
  requester: PagingRequester

  def __init__(self, cfg:PagingCfg):
    self.parsers = cfg.parsers
    self.requester = PagingRequester(cfg.links)
    self.cache_file_name = cfg.source+'.txt'
    self.cities = json.loads(cfg.cities_file_path.read_text())
    self.delay_interval = cfg.delay_interval

  def supports(self, car_type: CarType) -> bool:
    return car_type in self.parsers and car_type in self.requester.links
  
  async def get_post_urls(self, city:str, car_type:CarType) -> AsyncGenerator[str, None]:
    get_page:Callable[[int], str] = self.requester.get_pager(city, car_type)   
    url_counter = 0 
    for i in range(self.parsers[car_type].get_page_count(await get_page(1))):      
      list_page_content = await get_page(i+1)
      urls_list = self.parsers[car_type].parse_list_page(list_page_content)[:POST_LIMIT - url_counter]
      url_counter += len(urls_list)
      for url in urls_list:
        yield url
