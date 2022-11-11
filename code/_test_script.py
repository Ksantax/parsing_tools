from collecting import DromPostCollector
from tools import CarType
import json
import aiohttp
import asyncio


async def main():
  async with aiohttp.ClientSession() as session:
    collector = DromPostCollector(session)
    posts = await collector.collect_posts('zalari', CarType.SPEC)
    posts = list(map(lambda x: x.as_dict(), posts))
    with open('static\\zalari.spec.json', 'w+', encoding='utf-8') as file:
      json.dump(posts, file, ensure_ascii=False, indent=4)
    del posts

    posts = await collector.collect_posts('atagay', CarType.SPEC)
    posts = list(map(lambda x: x.as_dict(), posts))
    with open('static\\atagay.spec.json', 'w+', encoding='utf-8') as file:
      json.dump(posts, file, ensure_ascii=False, indent=4)
    del posts

    posts = await collector.collect_posts('alzamay', CarType.SPEC)
    posts = list(map(lambda x: x.as_dict(), posts))
    with open('static\\alzamay.spec.json', 'w+', encoding='utf-8') as file:
      json.dump(posts, file, ensure_ascii=False, indent=4)
    del posts

    posts = await collector.collect_posts('bohan', CarType.AUTO)
    posts = list(map(lambda x: x.as_dict(), posts))
    with open('static\\bohan.auto.json', 'w+', encoding='utf-8') as file:
      json.dump(posts, file, ensure_ascii=False, indent=4)
    del posts

    posts = await collector.collect_posts('alzamay', CarType.AUTO)
    posts = list(map(lambda x: x.as_dict(), posts))
    with open('static\\alzamay.auto.json', 'w+', encoding='utf-8') as file:
      json.dump(posts, file, ensure_ascii=False, indent=4)
    del posts

    posts = await collector.collect_posts('artemovskiy-irk', CarType.AUTO)
    posts = list(map(lambda x: x.as_dict(), posts))
    with open('static\\artemovskiy-irk.auto.json', 'w+', encoding='utf-8') as file:
      json.dump(posts, file, ensure_ascii=False, indent=4)
    del posts  


if __name__ == '__main__':
  asyncio.run(main())