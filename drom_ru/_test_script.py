import bs4
import json
import os
import requests

def collect_posts() -> list:
  return [parse_post(link) for link in get_post_links()]
  

def get_post_links() -> list:
  links = []
  i = 1
  while True:
    res = requests.get(f'https://kurchatov.drom.ru/auto/all/page{i}/?unsold=1')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    main_div = soup.select_one('div.css-1173kvb.eaczv700 div.css-1nvf6xk.eaczv700')
    if main_div is None or main_div.select_one('div.css-vsx4mr.e18vbajn0') is not None:
      break
    links += [a.get('href') for a in main_div.select('a.css-xb5nz8.ewrty961')]
    i += 1
  return links


def parse_post(post_url:str) -> dict:
  soup = bs4.BeautifulSoup(requests.get(post_url).text, 'lxml')
  return {
    "publishedAt": get_date(soup),
    "text": get_params_text(soup)+'\n\n'+\
            get_data_list_text(soup)+'\n\n'+\
            get_additional_info(soup),
    "city": get_city(soup),
    "url": post_url,
    "source": "drom.ru"
  }


def get_price(soup:bs4.BeautifulSoup):
  return soup.select_one('div.css-eazmxc.e162wx9x0').text.replace('\xa0', ' ')


def get_date(soup:bs4.BeautifulSoup):
  return soup.select_one('div.css-pxeubi.evnwjo70').text.split()[-1]


def get_params_text(soup:bs4.BeautifulSoup):
  res = []
  param_names = soup.select('th.css-16lvhul.ezjvm5n1')
  param_values = soup.select('td.css-9xodgi.ezjvm5n0')
  for n, v in zip(param_names, param_values):
    if v.string is None:
      if v.find('span') is not None:
        v = v.find('span')
      else:
        v = v.find('a')
    v_text = v.text
    if 'Мощ' in n.text:
      v_text = v_text.split(',')[0]
      v_text.replace('\xa0', ' ')
    res.append(f'{n.text}: {v_text}')
  return '\n'.join(res)


def get_data_list_text(soup:bs4.BeautifulSoup):
  data_list = soup.select('div.css-xvjsia.ei6sjku0 div')
  return '\n'.join({div.text for div in data_list if 'green' in str(div)})  


def get_additional_info(soup:bs4.BeautifulSoup):
  text_span = soup.select_one('div.css-inmjwf.e162wx9x0 span.css-1kb7l9z.e162wx9x0')
  return '' if not text_span else text_span.text


def get_city(soup:bs4.BeautifulSoup):
  return soup.select('div.css-inmjwf.e162wx9x0')[-1].text.split(':')[-1].strip()



if __name__ == '__main__':
  posts = collect_posts()
  with open(os.path.dirname(__file__)+'/static/_temp.json', 'w+', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=4)
