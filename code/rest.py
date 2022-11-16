from fastapi import FastAPI
import service
from tools import CarType


app = FastAPI()


@app.post("/reload_config")
def reload_config():
  service.reload_config()


@app.get("/posts/")
async def get_posts(city:str, car_type:CarType):
  return await service.get_posts(city, car_type)

