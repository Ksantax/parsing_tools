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
  source = 'avito',
  delay_interval = (3., 6.),
  cities_file_path = STATIC_DIR / 'avito_cities.json',
  headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': r'''u=2tkmhf3l.8qu3k8.nfdbcgtl1c00; _gcl_au=1.1.120033922.1667385451; _ym_uid=1667385451513748059; _ym_d=1667385451; _ga=GA1.1.1381121335.1667385451; __ddg1_=TMPNMOxKCnV1gGUGqNu2; uxs_uid=4b8b8680-67da-11ed-9877-f328466385fc; __zzatw-avito=MDA0dBA=Fz2+aQ==; __zzatw-avito=MDA0dBA=Fz2+aQ==; cfidsw-avito=jsJclK0QH6ls5pxBT3kRYzhANCvnWFbSH6OhTYTLGh1kgm2WDfqaMVeT2loxPSBM8GHSwMHDb7msThdunpt+BSQr32iooqo85N26oDtrPYT6mGQPAFnFvs2Snk7LND7E3Q/7cDL/8uxhchLsCkw+IgP35cjqON9jG1c0; cfidsw-avito=jsJclK0QH6ls5pxBT3kRYzhANCvnWFbSH6OhTYTLGh1kgm2WDfqaMVeT2loxPSBM8GHSwMHDb7msThdunpt+BSQr32iooqo85N26oDtrPYT6mGQPAFnFvs2Snk7LND7E3Q/7cDL/8uxhchLsCkw+IgP35cjqON9jG1c0; cfidsw-avito=jsJclK0QH6ls5pxBT3kRYzhANCvnWFbSH6OhTYTLGh1kgm2WDfqaMVeT2loxPSBM8GHSwMHDb7msThdunpt+BSQr32iooqo85N26oDtrPYT6mGQPAFnFvs2Snk7LND7E3Q/7cDL/8uxhchLsCkw+IgP35cjqON9jG1c0; adrcid=Anxkvoci4p3A9AZ-hV7ax8w; _ga_WW6Q1STJ8M=GS1.1.1668848401.2.1.1668848466.0.0.0; v=1669280276; _ym_visorc=b; _ym_isad=2; tmr_lvid=7995b2aceb400646446dfc52f39971b5; tmr_lvidTS=1667385451487; isCriteoSetNew=true; f=5.0c4f4b6d233fb90636b4dd61b04726f1277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb161277909827d0cb1610df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9ad42d01242e34c7968e2978c700f15b6bf11f980bc2bc377f2c082410b22639b04dbcad294c152cb0df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d20df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f642b81f1c77c4dcf4df4fb29506e8757e3cc66d11db4e86a598cd43f3547c68727617c7721dca45217b304f0a1efaa68cdcb3057378ed6936ff2ebf3cb6fd35a0ac0df103df0c26013a28a353c4323c7a3a140a384acbddd748317f4b21c920036c3de19da9ed218fe23de19da9ed218fe2b4af293ec419f67f6cd48844eb16d6d58edd6a0f40cbfd87da3d420d6cca468c; ft="lXfLz+Um1O8lUuksF+KG1KzXnH1AphWTU6/Jz8LQBUCR0vI4anuZ7spwx1Truc7gXa9wUqhz4m5wAWlDzZoNGpHJExwHVXsme8krx/hk9uvuIIgbHWqWWeAfjJSqTDnn/ukTGL8JQNnz1Qi8Ps2xdGMz9BFlCrVDg+3mbZE0SfMhavgkqN/oTPWb3ZFqLCwH"; buyer_laas_location=628810; dfp_group=100; buyer_location_id=628810; luri=angarsk; buyer_popup_location=628810; sx=H4sIAAAAAAAC%2F5yWSZLrSq%2BD91LjM8iGZJJ3N8xOtnrbshrfqL2%2F0I0ov%2FIZ%2Fhv4hAABKP%2F9MuikGJcNxGRTYQITVTByNVRcyl%2F%2F%2FPu1fv3z5TrnjxeGUdeVJU1x6yYd7OWR%2FXO1x9efr%2FL1jyUST2wAvv98mQJJUgFhSsGazIHFq7gqFEJS%2BCHjfbz2aSyvZl2SvV72y3idH1fPZgY7029ycMZ8%2F%2FmypuTiFKOzVJyAtVyjywAJKGOSH7J4H%2B1yfSxlLo88d2Pc4RB7zPb5yu6XZieB5D8yOEsQrBXnWMEpiNhgxAqVXOFNvvTuPvhng9Nih74Obln2Y5xThAHG6%2BWDbCicZKrJUk4u5OB9DT7Zoq6QUvKqOf6Qk0vtLVHInXSy1afPZHpCfCxti7R%2F%2BGydnOSqaAGTTaxI9J%2FlSdCbal2FEN4XbOZlKnWwISYs3mKdy2Wg2A5TxXH70BzMqdl76xWxoEQohZkYNCFFF33x6OsPebiOUqW5t9NwqS80ZoVqmvv2HPNRZ%2F7MhvMnGVyS6iN6L4bIi7WuZKt4ykKTfshLF5%2FdYW%2BH3rS7jUc0ZMr86kptsJ3dL7Kx7OxJ1sRZXTGqqAAMOQcpkbJxETC%2FNd%2F6pxCk8dUDd69hdAPojc2zKceY%2BtdfPp%2BagapISManVChlJ8hBJbhQPScD5Z3n8xy3XfZgt8lohR4mk2rs9%2F7Wpk8ywHlBCIgSBMh7reCRVaUYwkJJFVTfboxxUd%2FqY29Hvz2fnVPbycW1XbpOzUc2ziN%2B%2F%2FlCiSX5nIyNmX3RoBwsccpRAXzwP2RLIfPrwG6wt%2Be6vkbtV%2B1gvzWQs5rPPPPpM3nhHDOEwpUxSMnqOOSSUVkV8Yfsn2V%2F3HFob7XZLnwNN4PX55bLfXz0r88OGqGTTEQpB6pCggQkJcTiJQc0KYX87uBxYBu649r29so6c7842ZelpSkZmfHDDcBzkSgqWrFZGNWIT2g41GxiAkMh8P8vEs0FrtXsU32lPFwnQledh36iY%2FXT5264U3PA4jHWQFhsZfREkisgWaCcIL991r55lssGvhnBtdtd5zEWaPptxnWYbp8dxDN1YdFpTl3Ux8b8aKam2wASb%2BYdZLoM9yeNveaIy1LScp%2Fuyy1d%2FM69fX0grT2RDErBYYopSODI1lVKuSKAz1HSW2yfG7nh0DaXW%2FBQ9mccxv5R4bg%2B7o%2FDfpBB3PefLxGD0VZXMEVWH%2BD8A4hJUY0DT%2B9aX3X3YGrnhMzLxCPeB7gz3XEjufe%2Fa01E4TRYbuZw0a13aHjj9Ng2Bui2pntvfUJXk6rm7FExgqaYTDURYnBgSVPy6qB8liScUVYXMKVkQig2B6yWoNYKEMQaw0w%2Fn6h7zmvUa7POQB4vM%2FsD4t3WofavtfkryufvJNbIJZhiAxjMbKyJbFBCcVoTR%2FmfbmjOyYhXcvemfxzhsfFj2poOoOma7e3HMXZhgYhut9cVH8HTYx0fBgFZXhf9vZwG8Dxe9o7EZExZtXhB9UoOzokiU9m82zHz87nZdQjH0q%2F7XsxzCje4yytsvfH95yb7U2zx7F0JWBgcWuVis80hIroQC%2Fr3coZXGRy8LleM9dgxXzh0l21I0oyN7%2FWv3p2nK5FYHcWgKFmqKQ6qagohoaq6Xy8B6WHfV7l0qiMZmqCUocaNqdbkf2smD%2F4%2FspbAXApkxpgqAtWqhGhYJJe35kNMqf2xSHtvYzN1kF4wmD63nLHpy1%2Bvl9PnE1WkqBYmZM%2FJqpCzRMGK%2BPiO23gcJHif2ob21SpPfK21WZf1NfVN91ES8QZPMiMny1w925x9gWRMqskrQAQu%2FI6bIdf0mBT7RZ73xlTEamzjr%2BinLn76jGeQa8wFfcieorFRIrGpzkjCyCLq38WGMfM8Ph6euj1cZrO2TRitG4bWydz2n%2FvmzPf3%2FwUAAP%2F%2FyITdgIEKAAA%3D; abp=0; cto_bundle=diT4xl9HMFJ1R3NUUnpNbmRuJTJGN2E3SVU5M0hXdzlMd0Q5ejFQQ0YwY1RMQVFoaHREb3NIRW9rS3BIVDRvZjM4dWNuNlVneHI0Q2VKYjJLNFBaQUV2NGFQSVhNZmVlJTJGbTNZOG9PYUxqd1hSWCUyRklCdG8xU240JTJGRmZpMVlSa3ZOWWhKV1RhRyUyRnFyVk1DNTFkViUyRjlMOXlLRGh1SHclM0QlM0Q; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyRnJpJTJDJTIwMjQlMjBOb3YlMjAyMDIzJTIwMDklM0E0NCUzQTE2JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyNjU0YTg2NmM0YzY1NjdlNzhhNWNiNTdkYzQ2MTRjMjMlNUMlMjIlMkMlNUMlMjJmcGpzRm9ybWF0JTVDJTIyJTNBdHJ1ZSU3RCUyMiU3RA==; tmr_detect=0%7C1669283058017; _ga_M29JC28873=GS1.1.1669280278.19.1.1669283062.52.0.0; _ga_9E363E7BES=GS1.1.1669280278.18.1.1669283062.52.0.0''',
    'referer': 'https://www.avito.ru',
  },
  parsers_links = {
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
  PagingPostCollector(AVITO_CFG)
]
