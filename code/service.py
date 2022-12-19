from .tools import CarType, Post
from .instances import COLLECTORS
import traceback
from typing import AsyncGenerator
from asyncio import create_task, Task


async def __collect(acc:list[dict], gen:AsyncGenerator[Post, None]) -> None:
  async for x in gen:
    acc.append(x.as_dict())


def create_tasks(response:list, city:str, car_type:CarType) -> list[tuple[str, Task]]:
  tasks = []
  for collector in COLLECTORS:
    if collector.supports(car_type):
      task = create_task(__collect(response, collector.collect_posts(city, car_type)))
      collector_name = collector.name
      tasks.append((collector_name, task))
  return tasks


async def get_posts(city:str, car_type:CarType) -> list[dict]:
  response = []
  tasks = create_tasks(response, city, car_type)
  
  for collector_name, task in tasks:
    try:
      await task
    except Exception:
      print(f">>>> city={city}, car_type={car_type.value}")
      print(f">>>> Exception from collector {collector_name}")
      print(traceback.format_exc())
      continue
  return response
