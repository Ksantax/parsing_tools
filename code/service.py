import aiohttp
from typing import Generator
from .tools import CarType
from .collecting import PostCollector
from importlib import reload
from . import config
import asyncio_atexit


COLLECTORS:list[PostCollector] = []
SESSION:aiohttp.ClientSession = None


async def get_posts(city:str, car_type:CarType) -> Generator[list[dict], tuple[str, CarType], None]:
  global COLLECTORS, SESSION
  if not SESSION:
    SESSION = aiohttp.ClientSession()
    asyncio_atexit.register(SESSION.close)
    reload_config()
  try:
    response = []
    for collector in COLLECTORS:
      async for post in collector.collect_posts(city, car_type):
        response.append(post.as_dict())
    return response
  except Exception:
    return []


def reload_config() -> None:
  global COLLECTORS
  reload(config)
  COLLECTORS = list(map(lambda cl: cl(SESSION), config.collectors))

  
