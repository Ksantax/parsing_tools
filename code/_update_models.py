import bs4
import json
import os

'''
Предварительно нужно скачать html главной страницы drom.ru
с развёрнутым списком моделей. Те модели, которых там нет 
добавлялись в ручную, прокликивая в фильтрах поиска те, объявлений
о продаже которых нет (серые).
'''

MODELS_JSON_PATH = os.path.dirname(__file__)+'\\static\\drom_auto_models.json'
MAIN_PAGE_WITH_EXPANDED_MODEL_LIST_FILE = os.path.dirname(__file__)+'\\static\\_temp.html'


def update_models():
  with open(MAIN_PAGE_WITH_EXPANDED_MODEL_LIST_FILE, 'r') as file:
    page_text = file.read()
  soup = bs4.BeautifulSoup(page_text, 'lxml')
  models = dict()
  for a in soup.select('div.css-ofm6mg.exkrjba0 a'):
    models[a.text.strip().lower()] = a.get('href').split('/')[-2]
  save_models(models)


def save_models(models:dict) -> None:
  if os.path.exists(MODELS_JSON_PATH):
    with open(MODELS_JSON_PATH, 'r', encoding='utf-8') as f:
      old_models = json.load(f)
    models.update(old_models)
  
  with open(MODELS_JSON_PATH, 'w+', encoding='utf-8') as f:
    json.dump(models, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
  update_models()

