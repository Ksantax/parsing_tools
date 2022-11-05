from enum import Enum
from collections import namedtuple
from datetime import datetime

Post = namedtuple('Post', ['publishedAt'])

class CarType(Enum):
  AUTO = "Легковое авто"
  SPEC = "Спецтехника/Грузовики"
  MOTO = "Мотоцикты"

class DataSourse(Enum):
  DROM_RU = 'drom.ru'