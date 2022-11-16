import aiohttp
from .errors import BadResponseStatus
from .tools import CarType
from typing import Callable
from fake_headers import Headers


class Requester:
  session: aiohttp.ClientSession
  headers = Headers()
  def __init__(self, session:aiohttp.ClientSession):
    self.session = session
  
  async def get(self, url:str) -> str:
    async with self.session.get(url, headers=self.headers.generate()) as response:
      if response.status != 200:
        raise BadResponseStatus('Got not 200 response status while getting: '+url)
      return await response.text()


class DromRequester(Requester):
  session: aiohttp.ClientSession
  list_urls:dict[CarType, str] = {
    CarType.AUTO: 'https://{}.drom.ru/auto/all/page{}/?unsold=1',
    CarType.SPEC: 'https://{}.drom.ru/spec/all/page{}/?unsold=1',
    CarType.MOTO: 'https://moto.drom.ru/{}/sale/?page={}',
  }
  
  def get_pager(self, city:str, car_type:CarType) -> Callable[[int], str]:
    async def pager(page_number:int) -> str:
      return await self.get(self.list_urls[car_type].format(city, page_number))
    return pager
    

