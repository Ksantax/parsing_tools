from tools import CarType
import json
import asyncio
import service

async def main():
  await service.init_app()
  posts = await service.get_posts('alzamay', CarType.SPEC)
  for post in posts:
    print(json.dumps(post, ensure_ascii=False, indent=4, sort_keys=True))

if __name__ == '__main__':
  asyncio.run(main())