import bs4
from tools import CarType, Post
import math


class Parser:
  def parse_post(self, post_page_text:str) -> Post:
    raise NotImplementedError
  

  def __call__(self, post_page_text:str) -> Post:
    return self.parse_post(post_page_text)


class DromParser(Parser):
  def get_page_count(self, list_page_text:str) -> int:
    raise NotImplementedError
  
  def parse_list(self, list_page_text:str) -> list[str]:
    raise NotImplementedError


class DromPagingParser(Parser):
  POST_PER_PAGE = 20

  def parse_post(self, post_page_text:str) -> Post:
    soup = bs4.BeautifulSoup(post_page_text, 'lxml')
    return Post (
      publishedAt = self.__get_date(soup),
      price = self.__get_price(soup),
      text = self.__get_text(soup),
      properties = self.__get_properties(soup),
      source = "drom.ru"
    )

  def __get_price(self, soup:bs4.BeautifulSoup):
    return soup.select_one('div.css-eazmxc.e162wx9x0').text.replace('\xa0', ' ')

  def __get_date(self, soup:bs4.BeautifulSoup):
    return soup.select_one('div.css-pxeubi.evnwjo70').text.split()[-1]

  def __get_properties(self, soup:bs4.BeautifulSoup):
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

  def __get_text(self, soup:bs4.BeautifulSoup):
    return self.__get_title(soup)+'\n\n'+\
           self.__get_main_text(soup)+'\n\n'+\
           self.__get_green_checks(soup)
  
  def __get_title(self, soup:bs4.BeautifulSoup) -> str:
    return soup.select_one('span.css-1kb7l9z.e162wx9x0').text

  def __get_main_text(self, soup:bs4.BeautifulSoup):
    text_span = soup.select_one('div.css-inmjwf.e162wx9x0 span.css-1kb7l9z.e162wx9x0')
    return ('' if not text_span else text_span.text)
  
  def __get_green_checks(self, soup:bs4.BeautifulSoup):
    data_list = soup.select('div.css-xvjsia.ei6sjku0 div')
    return '\n'.join({div.text for div in data_list if 'green' in str(div)})  

  def get_page_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.select_one('div#tabs a')
    return math.ceil((int(tag.text.split()[0]) if tag else 0) / self.POST_PER_PAGE)
  
  def parse_list(self, car_type, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    main_div = soup.select_one('div.css-1173kvb.eaczv700 div.css-1nvf6xk.eaczv700')
    return [a.get('href') for a in main_div.select('a.css-xb5nz8.ewrty961')]


class DromScrollingParser(Parser):
  POST_PER_PAGE = 50

  def parse_post(self, post_page_text:str) -> Post:
    soup = bs4.BeautifulSoup(post_page_text, 'lxml')
    return Post (
      publishedAt = self.__get_date(soup),
      price = self.__get_price(soup),
      text = self.__get_text(soup),
      properties = self.__get_properties(soup),
      source = "drom.ru"
    )
  
  def __get_price(self, soup:bs4.BeautifulSoup):
    return soup.select_one('div.css-eazmxc.e162wx9x0').text.replace('\xa0', ' ')

  def __get_date(self, soup:bs4.BeautifulSoup):
    return soup.select_one('div.css-pxeubi.evnwjo70').text.split()[-1]

  def __get_properties(self, soup:bs4.BeautifulSoup):
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

  def __get_text(self, soup:bs4.BeautifulSoup):
    return self.__get_title(soup)+'\n\n'+\
           self.__get_main_text(soup)+'\n\n'+\
           self.__get_green_checks(soup)
  
  def get_page_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.select_one('span#itemsCount_placeholder strong')
    return math.ceil((int(tag.text.split()[0]) if tag else 0) / self.POST_PER_PAGE)

  def parse_list(self, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag_list = soup.select('tbody.native tr:not([data-accuracy]) a.bulletinLink')
    return ['https://moto.drom.ru'+a.get('href') for a in tag_list]




  

