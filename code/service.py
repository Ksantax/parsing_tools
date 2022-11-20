import aiohttp
from .tools import CarType
from .collecting import PostCollector, DromPostCollector
import asyncio_atexit
from .errors import NotSupportedCarType, BadResponseStatus
from typing import Callable, TypeVar, ParamSpec
T, P = TypeVar('T'), ParamSpec('P')


COLLECTOR_CLASSES:list = [DromPostCollector]
COLLECTORS:list[PostCollector] = []


def inited(func: Callable[P, T]) -> Callable[P, T]:
  def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
    if not COLLECTORS:
      for cl in COLLECTOR_CLASSES:
        session = aiohttp.ClientSession()
        asyncio_atexit.register(session.close)
        COLLECTORS.append(cl(session))
    return func(*args, **kwargs)
  return wrapper


@inited
async def get_posts(city:str, car_type:CarType) -> list[dict[str, str|dict[str, str]]]:
  response = []
  for collector in COLLECTORS:
    try:
      async for post in collector.collect_posts(city, car_type):
        response.append(post.as_dict())
    except:
      pass
  return response


