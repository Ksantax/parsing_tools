import aiohttp
from .errors import BadResponseStatus, NotSupportedCarType
from .tools import CarType
from typing import Callable
from fake_headers import Headers
from .configurating import PagingCfg
import asyncio_atexit
from typing import Callable, TypeVar, ParamSpec
T, P = TypeVar('T'), ParamSpec('P')

import ssl
import asyncio
import sys
CIPHERS = ':'.join([
    'ECDHE-ECDSA-AES128-GCM-SHA256', 'ECDHE-RSA-AES128-GCM-SHA256', 'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384', 'ECDHE-ECDSA-CHACHA20-POLY1305', 'ECDHE-RSA-CHACHA20-POLY1305',
    'DHE-RSA-AES128-GCM-SHA256', 'DHE-RSA-AES256-GCM-SHA384', 'DHE-RSA-CHACHA20-POLY1305', 'ECDHE-ECDSA-AES128-SHA256',
    'ECDHE-RSA-AES128-SHA256', 'ECDHE-ECDSA-AES128-SHA', 'ECDHE-RSA-AES128-SHA', 'ECDHE-ECDSA-AES256-SHA384',
    'ECDHE-RSA-AES256-SHA384', 'ECDHE-ECDSA-AES256-SHA', 'ECDHE-RSA-AES256-SHA', 'DHE-RSA-AES128-SHA256',
    'DHE-RSA-AES256-SHA256', 'AES128-GCM-SHA256', 'AES256-GCM-SHA384', 'AES128-SHA256', 'AES256-SHA256', 'AES128-SHA',
    'AES256-SHA', 'DES-CBC3-SHA'
])


class Requester:
  session: aiohttp.ClientSession = None
  headers_generator = Headers(headers=True)
  const_headers:dict[str, str] = None

  def inited(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> T:
      if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
      if not self.session:
        ctx = ssl.create_default_context()
        ctx.options |= (ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        ctx.set_ciphers(CIPHERS)
        ctx.verify_mode = ssl.CERT_REQUIRED
        con = aiohttp.TCPConnector(ssl=ctx)
        self.session = aiohttp.ClientSession(connector=con)
        asyncio_atexit.register(self.session.close)
      return func(self, *args, **kwargs)
    return wrapper

  @inited
  async def get(self, url:str) -> str:
    async with self.session.get(url, headers=self.headers) as response:
      if response.status != 200:
        raise BadResponseStatus(f'Got {response.status} response status while getting: '+url)
      return await response.text()
  
  @property
  def headers(self):
    headers = self.headers_generator.generate()
    if self.const_headers:
      for header, value in self.const_headers.items():
        headers[header] = value
    return headers


class PagingRequester(Requester):
  links:dict[CarType, str]

  def __init__(self, cfg:PagingCfg):
    self.links = cfg.links
    self.const_headers = cfg.headers

  def get_pager(self, city:str, car_type:CarType) -> Callable[[int], str]:
    if car_type not in self.links:
      raise NotSupportedCarType(f'Not supported {car_type} for {type(self)} requester')
    async def pager(page_number:int) -> str:
      return await self.get(self.links[car_type].format(city, page_number))
    return pager
