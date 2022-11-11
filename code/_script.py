from tools import CarType
import json
import asyncio

async def main():
  import service
  service.init_collectors()
  posts = await service.get_posts('alzamay', CarType.SPEC)
  for post in posts:
    print(json.dumps(post, ensure_ascii=False, indent=4, sort_keys=True))

if __name__ == '__main__':
  asyncio.run(main())