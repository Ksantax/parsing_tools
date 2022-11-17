from fastapi import FastAPI
from .tools import CarType
from . import service 


app = FastAPI()


@app.get("/posts/")
async def get_posts(city:str, car_type:CarType):
  return await service.get_posts(city, car_type)
