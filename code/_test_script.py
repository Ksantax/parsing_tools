from selenium import webdriver
from time import sleep
import bs4

# driver = webdriver.Chrome(executable_path='C:\\Programming\\VITYAZ\\parsing_tools\\chromedriver\\chromedriver.exe')
# driver.get('https://moto.drom.ru/bodaibo/sale/')

# sleep(20)

# with open('static\\_temp.html', 'w+', encoding="utf-8") as file:
#   file.write(driver.page_source)

with open('static\\_temp.html', 'r', encoding="utf-8") as file:
  html = file.read()


soup = bs4.BeautifulSoup(html, 'lxml')


print([a.get('href') for a in soup.select('tbody.native tr:not([data-accuracy]) a.bulletinLink')], sep='\n')