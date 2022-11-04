import bs4
import json
import os
import requests


#container_selector = 'div.css-1173kvb.eaczv700 div.css-1nvf6xk.eaczv700'
#title_selector = 'div.css-vsx4mr.e18vbajn0'
#a_selector = 'a.css-xb5nz8.ewrty961'
#
#links = []
#i = 1
#while True:
#  res = requests.get(f'https://kurchatov.drom.ru/auto/all/page{i}/?unsold=1')
#  soup = bs4.BeautifulSoup(res.text, 'lxml')
#  main_div = soup.select_one(container_selector)
#  if main_div is None or main_div.select_one(title_selector) is not None:
#    break
#  new_links = [a.get('href') for a in main_div.select(a_selector)]
#  
#  print(f'page {i}')
#  print(*new_links, sep='\n')
#  print()
#  links += new_links
#  i += 1




# url = 'https://kurchatov.drom.ru/lada/2107/48584167.html'
# file_path = os.path.join(os.path.dirname(__file__), 'static\\_temp.html')
# page_text = requests.get(url).text
# with open(file_path, 'w+') as f:
#   f.write(page_text)


file_path = os.path.join(os.path.dirname(__file__), 'static\\_temp.html')
with open(file_path, 'r') as f:
  page_text = f.read()

soup = bs4.BeautifulSoup(page_text, 'lxml')

date_selector = 'div.css-pxeubi.evnwjo70'
price_selector = 'div.css-eazmxc.e162wx9x0'
param_names_selector = 'th.css-16lvhul.ezjvm5n1'
param_values_selector = 'td.css-9xodgi.ezjvm5n0'

def get_params_text():
  res = []
  for n, v in zip(soup.select(param_names_selector), soup.select(param_values_selector)):
    if v.string is None:
      if v.find('span') is not None:
        v = v.find('span')
      else:
        v = v.find('a')
    res.append(f'{n.text}: {v.text}')
  return '\n'.join(res)

print(get_params_text())

# print(*[(n.text, v.text) for n, v in zip(soup.select(param_names_selector),
                              #  soup.select(param_values_selector))], sep='\n')

'''
{
  "id": "",
  "userId": "",
  "publishedAt": "",
  "text": "",
  "city": "",
  "contacts": "",
  "url": "",
  "source": ""
}
'''
