import bs4
import requests
import json
import os

CITIES_JSON_PATH = os.path.dirname(__file__)+'\\static\\drom_auto_cities.json'


# {'region>city': 'href'}
def get_cities(*, update:bool = False) -> dict[str: str]:
  if update:
    return update_cities(return_cities=True)
  else:
    return _load_cities_form_file()
  

def update_cities(*, return_cities:bool = False) -> None:
  cities_page = requests.get('https://auto.drom.ru/cities/').text
  cities = _parse_cities_page(cities_page)
  _save_cities_to_file(cities)
  if return_cities:
    return cities


def _parse_cities_page(page:str) -> str:
  soup = bs4.BeautifulSoup(page, 'lxml')
  resault = dict()
  main_div = soup.select_one('div.b-selectCars.b-media-cont')
  for region_div in main_div.select('div.b-selectCars__item'):
    if region_div.get('data-region-id'):    # May be
      resault.update(_parse_region(region_div))
  return resault


def _parse_region(region_div:bs4.element.Tag) -> dict[str: str]:
  resault = dict()
  region_name = region_div.select_one('a').text.strip().lower()
  for a in region_div.find_next('noscript').select('a'):
    if 'region' not in a.get('href'):
      resault[f'{region_name}>{a.text.strip().lower()}'] = a.get('href')
  return resault


def _save_cities_to_file(cities:dict, file_name:str = CITIES_JSON_PATH) -> None:
  with open(file_name, 'w+', encoding='utf-8') as f:
    json.dump(cities, f, ensure_ascii=False, indent=4)

def _load_cities_form_file(file_name:str = CITIES_JSON_PATH) -> dict:
  with open(file_name, 'r', encoding='utf-8') as f:
    res = json.load(f)
  return res


if __name__ == '__main__':
  cities = get_cities(update=True)
