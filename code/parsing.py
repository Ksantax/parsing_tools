import bs4
from .tools import Post
import math


class Parser:
  def parse_post(self, post_page_text:str) -> Post:
    raise NotImplementedError
  

  def __call__(self, post_page_text:str) -> Post:
    return self.parse_post(post_page_text)


class DromParser(Parser):
  def parse_post(self, post_page_text:str) -> Post:
    soup = bs4.BeautifulSoup(post_page_text, 'lxml')
    return Post (
      publishedAt = self._get_date(soup),
      price = self._get_price(soup),
      text = self._get_text(soup),
      properties = self._get_properties(soup),
      source = "drom.ru"
    )

  def _get_price(self, soup:bs4.BeautifulSoup) -> str:
    raise NotImplementedError

  def _get_date(self, soup:bs4.BeautifulSoup) -> str:
    raise NotImplementedError

  def _get_properties(self, soup:bs4.BeautifulSoup) -> dict[str, str]:
    raise NotImplementedError

  def _get_text(self, soup:bs4.BeautifulSoup) -> str:
    raise NotImplementedError  

  def get_page_count(self, list_page_text:str) -> int:
    raise NotImplementedError
  
  def parse_list(self, list_page_text:str) -> list[str]:
    raise NotImplementedError


class DromPagingParser(DromParser):
  POST_PER_PAGE = 20

  def _get_price(self, soup:bs4.BeautifulSoup) -> str:
    return soup.select_one('div.css-eazmxc.e162wx9x0').text.replace('\xa0', ' ')

  def _get_date(self, soup: bs4.BeautifulSoup) -> str:
    return soup.select_one('div.css-pxeubi.evnwjo70').text.split()[-1]
  
  def _get_properties(self, soup:bs4.BeautifulSoup) -> dict[str, str]:
    props = dict()
    param_names = soup.select('th.css-16lvhul.ezjvm5n1')
    param_values = soup.select('td.css-9xodgi.ezjvm5n0')
    for n, v in zip(param_names, param_values):
      if v.text is None:
        if v.find('span') is not None:
          v = v.find('span')
        else:
          v = v.find('a')
      v_text = v.text
      if 'Мощность' in n.text:
        v_text = v_text.split(',')[0]
      v_text.replace('\xa0', ' ')
      props[n.text] = v_text
    return props

  def _get_text(self, soup:bs4.BeautifulSoup) -> str:
    return self.__get_title(soup)+'\n\n'+\
           self.__get_main_text(soup)+'\n\n'+\
           self.__get_green_checks(soup)
  
  def __get_title(self, soup:bs4.BeautifulSoup) -> str:
    return soup.select_one('span.css-1kb7l9z.e162wx9x0').text

  def __get_main_text(self, soup:bs4.BeautifulSoup) -> str:
    text_span = soup.select_one('div.css-inmjwf.e162wx9x0 span.css-1kb7l9z.e162wx9x0')
    return ('' if not text_span else text_span.text)
  
  def __get_green_checks(self, soup:bs4.BeautifulSoup) -> str:
    data_list = soup.select('div.css-xvjsia.ei6sjku0 div')
    return '\n'.join({div.text for div in data_list if 'green' in str(div)})  

  def get_page_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.find('div', id='tabs')
    return math.ceil((int(tag.text.split()[0]) if tag else 0) / self.POST_PER_PAGE)
  
  def parse_list(self, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    main_div = soup.select_one('div.css-1173kvb.eaczv700 div.css-1nvf6xk.eaczv700')
    return [a.get('href') for a in main_div.select('a.css-xb5nz8.ewrty961')]


class DromScrollingParser(DromParser):
  POST_PER_PAGE = 50
  
  def _get_price(self, soup:bs4.BeautifulSoup):
    return soup.find('span', {'data-field': 'price'}).text

  def _get_date(self, soup:bs4.BeautifulSoup):
    return soup.find('div', class_='viewbull-actual-date').text

  def _get_properties(self, soup:bs4.BeautifulSoup):
    prop_divs = soup.find_all('div', class_='field viewbull-field__container')
    return {div.div.text.strip(): div.find('div', class_='value').text.strip()
        for div in prop_divs}

  def _get_text(self, soup:bs4.BeautifulSoup):
    title = soup.find('span', {'data-field':'subject'}).text.strip()
    text_divs = soup.find_all('div', class_='field text viewbull-field__container')
    text = '\n'.join(f'{div.h3.text.strip()}: \n{div.p.text.strip()}' for div in text_divs)
    return f'{title}\n\n{text}'
  
  def get_page_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.select_one('span#itemsCount_placeholder strong')
    return math.ceil((int(tag.text.split()[0]) if tag else 0) / self.POST_PER_PAGE)

  def parse_list(self, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag_list = soup.select('tbody.native tr:not([data-accuracy]) a.bulletinLink')
    return ['https://moto.drom.ru'+a.get('href') for a in tag_list]




  

