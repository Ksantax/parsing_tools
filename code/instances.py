from .parsing import DromNewDesignParser, DromOldDesignParser, AvitoParser
from .collecting import PostCollector, PagingPostCollector
from .tools import CarType
from .config import STATIC_DIR
from .configurating import PagingCfg


DROM_CFG:PagingCfg = PagingCfg( 
  source='drom',
  cities_file_path=STATIC_DIR / 'drom_cities.json',
  parsers_links={
    CarType.AUTO: (
      DromNewDesignParser(), 
      'https://{}.drom.ru/auto/all/page{}/?unsold=1'
    ),
    CarType.SPEC: (
      DromNewDesignParser(), 
      'https://{}.drom.ru/spec/all/page{}/?unsold=1'
    ),
    # CarType.MOTO: (
    #   DromOldDesignParser(), 
    #   'https://moto.drom.ru/{}/sale/?page={}'
    # )
  }
)

AVITO_CFG:PagingCfg = PagingCfg(
  source='avito',
  delay_interval=(3., 6.),
  cities_file_path= STATIC_DIR / 'avito_cities.json',
  parsers_links={
    CarType.AUTO: (
      AvitoParser(), 
      'https://www.avito.ru/{}/avtomobili?s=104&radius=0&localPriority=1&p={}'
    ),
    CarType.SPEC: (
      AvitoParser(), 
      'https://www.avito.ru/{}/gruzoviki_i_spetstehnika?s=104&radius=0&localPriority=1&p={}'
    ),
    CarType.MOTO: (
      AvitoParser(), 
      'https://www.avito.ru/{}/mototsikly_i_mototehnika?s=104&radius=0&localPriority=1&p={}'
    )
  }
)

COLLECTORS:list[PostCollector] = [
  PagingPostCollector(DROM_CFG),
  # PagingPostCollector(AVITO_CFG)   --- there is no cities file. I will get it on 2022.11.24
]
