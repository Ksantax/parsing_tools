import aiohttp
from collecting import PostCollector
from typing import Generator
from tools import CarType
from importlib import reload
import config
import asyncio_atexit
import asyncio


COLLECTORS:list[PostCollector] = []
SESSION:aiohttp.ClientSession = None


async def get_posts(city:str, car_type:CarType) -> Generator[list[dict], tuple[str, CarType], None]:
  global COLLECTORS
  try:
    response = []
    for collector in COLLECTORS:
      async for post in collector.collect_posts(city, car_type):
        response.append(post.as_dict())
    return response
  except Exception:
    return []


async def init_app():
  global SESSION
  if SESSION:
    SESSION.close()
  SESSION = aiohttp.ClientSession()
  asyncio_atexit.register(SESSION.close)
  reload_config()
  await asyncio.sleep(0)


def reload_config() -> None:
  global COLLECTORS
  reload(config)
  COLLECTORS = list(map(lambda cl: cl(SESSION), config.collectors))

  
