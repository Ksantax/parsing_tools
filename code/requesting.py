import aiohttp
from errors import BadResponseStatus
from tools import CarType
from typing import Callable
from fake_headers import Headers


class Requester:
  # TODO: 
  session: aiohttp.ClientSession
  headers = Headers()
  def __init__(self):
    self.session = aiohttp.ClientSession()
  
  async def get(self, url:str) -> str:
    async with self.session.get(url, headers=self.headers.generate()) as response:
      if response.status != 200:
        raise BadResponseStatus('Got not 200 response status while getting: '+url)
      return await response.text()
  
  def __del__(self):
    try:
      self.session.close()
    except:
      pass


class DromRequester(Requester):
  session: aiohttp.ClientSession
  list_urls:dict[CarType, str] = {
    CarType.AUTO: 'https://{city}.drom.ru/auto/all/page{page_number}/?unsold=1',
    CarType.SPEC: 'https://{city}.drom.ru/spec/all/page{page_number}/?unsold=1',
    CarType.MOTO: 'https://moto.drom.ru/{city}/sale/?page={page_number}',
  }

  def __init__(self):
    super().__init__()
  
  def get_pager(self, city:str, car_type:CarType) -> Callable[[int], str]:
    async def pager(page_number:int) -> str:
      return self.get(self.list_urls[car_type].format(city, page_number))
    return pager
    

