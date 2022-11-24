from .tools import CarType
from .instances import COLLECTORS
import traceback


async def get_posts(city:str, car_type:CarType) -> list[dict[str, str|dict[str, str]]]:
  response = []
  
  for collector in COLLECTORS:
    if not collector.supports(car_type):
      continue
    try:
      async for post in collector.collect_posts(city, car_type):
        response.append(post.as_dict())
    except Exception:
      print(f">>>> city={city}, car_type={car_type.value}")
      print(f">>>> Exception from collector {type(collector)}")
      print(traceback.format_exc())
      continue    
  return response
