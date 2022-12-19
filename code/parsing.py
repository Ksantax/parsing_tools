import bs4
from .tools import Post
import math
from .config import POST_LIMIT


class Parser:
  source: str

  def parse_post(self, post_page_text:str) -> Post:
    soup = bs4.BeautifulSoup(post_page_text, 'lxml')
    return Post (
      publishedAt = self._get_date(soup),
      price = self._get_price(soup),
      text = self._get_text(soup),
      properties = self._get_properties(soup),
      source = self.source
    )
    
  def _get_price(self, soup:bs4.BeautifulSoup) -> str:
    raise NotImplementedError

  def _get_date(self, soup:bs4.BeautifulSoup) -> str:
    raise NotImplementedError

  def _get_properties(self, soup:bs4.BeautifulSoup) -> dict[str, str]:
    raise NotImplementedError

  def _get_text(self, soup:bs4.BeautifulSoup) -> str:
    raise NotImplementedError 
  
  def __call__(self, post_page_text:str) -> Post:
    return self.parse_post(post_page_text)


class PaigingParser(Parser):
  post_per_page: int

  def get_page_count(self, list_page_text:str) -> int:
    total_posts = self._get_post_count(list_page_text)
    return min(math.ceil(POST_LIMIT / self.post_per_page), 
              math.ceil(total_posts / self.post_per_page))

  def _get_post_count(self, list_page_text:str) -> int:
    raise NotImplementedError

  def parse_list_page(self, list_page_text:str) -> list[str]:
    raise NotImplementedError


class DromParser(PaigingParser):
  source: str = 'drom.ru'


class DromNewDesignParser(DromParser):
  post_per_page = 20

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

  def _get_post_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.select_one('div#tabs div.css-1ksi09z.e1hsrrag2')
    if tag:
      total_posts = ''.join([num for num in tag.text.split() if num.isdigit()])
      return int(total_posts)
    return 0
  
  def parse_list_page(self, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    main_div = soup.select_one('div.css-1173kvb.eaczv700 div.css-1nvf6xk.eaczv700')
    return [a.get('href') for a in main_div.select('a.css-xb5nz8.ewrty961')]


class DromOldDesignParser(DromParser):
  POST_PER_PAGE = 50
  
  def _get_price(self, soup:bs4.BeautifulSoup):
    return soup.find('span', {'data-field': 'price'}).text

  def _get_date(self, soup:bs4.BeautifulSoup):
    return soup.find('div', class_='viewbull-actual-date').text

  def _get_properties(self, soup:bs4.BeautifulSoup):
    prop_divs = soup.select('div.field.viewbull-field__container')
    return {div.div.text.strip(): div.find('div', class_='value').text.strip()
        for div in prop_divs}

  def _get_text(self, soup:bs4.BeautifulSoup):
    title = soup.find('span', {'data-field':'subject'}).text.strip()
    text_divs = soup.select('div.field.text.viewbull-field__container')
    text = '\n'.join(f'{div.h3.text.strip()}: \n{div.p.text.strip()}' for div in text_divs)
    return f'{title}\n\n{text}'
  
  def _get_post_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.select_one('span#itemsCount_placeholder strong')
    if tag:
      return int(''.join([c for c in tag.text if c.isdigit()]))
    return 0

  def parse_list_page(self, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag_list = soup.select('tbody.native tr:not([data-accuracy]) a.bulletinLink')
    return ['https://moto.drom.ru'+a.get('href') for a in tag_list]


class AvitoParser(PaigingParser):
  source: str = 'avito.ru'
  post_per_page: int = 50

  def _get_price(self, soup:bs4.BeautifulSoup) -> str:
    try:
      price = soup.find('span', {'itemprop': 'price'}).get('content')
      currency = soup.find('meta', {'itemprop': 'priceCurrency'}).get('content')
      return price + ' ' + currency
    except:
      return 'N/A'

  def _get_date(self, soup:bs4.BeautifulSoup) -> str:
    date = soup.find('span', {'data-marker': 'item-view/item-date'}).text
    return date.replace('·', ' ').strip().lower()

  def _get_properties(self, soup:bs4.BeautifulSoup) -> dict[str, str]:
    li_tags = soup.select('li.params-paramsList__item-appQw')
    return {prop: val for prop, val in map(lambda li: li.text.split(': '), li_tags)}

  def _get_text(self, soup:bs4.BeautifulSoup) -> str:
    title = soup.find('span', {'itemprop': 'name', 'class': 'title-info-title-text'}).text
    text = soup.find('div', {'data-marker': 'item-view/item-description'}).text
    return title+'\n\n'+text
  
  def _get_post_count(self, list_page_text:str) -> int:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    tag = soup.find('span', {'data-marker': 'page-title/count'})
    if tag:
      return int(''.join([c for c in tag.text if c.isdigit()]))
    return 0

  def parse_list_page(self, list_page_text:str) -> list[str]:
    soup = bs4.BeautifulSoup(list_page_text, 'lxml')
    div = soup.find('div', {'data-marker': 'catalog-serp'})
    a_list:list[bs4.Tag] = div.find_all('a', {'itemprop': 'url', 'data-marker': 'item-title'})
    return [f"https://www.avito.ru{a.get('href')}" for a in a_list]
