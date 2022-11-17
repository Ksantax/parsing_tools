import aiohttp
from typing import Generator
from .tools import CarType
from .collecting import PostCollector, DromPostCollector
import asyncio_atexit


COLLECTOR_CLASSES:list = [DromPostCollector]
COLLECTORS:list[PostCollector] = []
SESSION:aiohttp.ClientSession = None


async def get_posts(city:str, car_type:CarType) -> Generator[list[dict], tuple[str, CarType], None]:
  global COLLECTORS, SESSION
  if not SESSION:
    SESSION = aiohttp.ClientSession()
    asyncio_atexit.register(SESSION.close)
    COLLECTORS = [cl(SESSION) for cl in COLLECTOR_CLASSES]
  response = []
  for collector in COLLECTORS:
    async for post in collector.collect_posts(city, car_type):
      response.append(post.as_dict())
  return response
