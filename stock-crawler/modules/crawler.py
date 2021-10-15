from bs4 import BeautifulSoup

from .logger import log

def crawl_stock_price(http_client, stock_name: str) -> str:
  page = http_client.request(
    'GET',
    'https://statusinvest.com.br/acoes/{}'.format(stock_name)
  )
  log(page)

  if not (page.status >= 200 and page.status < 300):
    return None

  data = BeautifulSoup(page.data, 'lxml')
  div_current = data.find_all('div', title='Valor atual do ativo')
  if div_current is None:
    return None

  for element in div_current:
    if element.find_next('strong') is not None:
      stock_price = element.find_next('strong').get_text()
      return stock_price

  return None
