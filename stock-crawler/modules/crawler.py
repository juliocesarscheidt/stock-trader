import json

from bs4 import BeautifulSoup

from .logger import log
from .utils import convert_value_to_float

def get_dolar_price(http_client) -> float:
  code = 'USD-BRL'
  api_uri = 'https://economia.awesomeapi.com.br/all'
  response = http_client.request('GET', f'{api_uri}/{code}')
  if not (response.status >= 200 and response.status < 300):
    return None
  data = json.loads(response.data)
  return convert_value_to_float(data['USD']['ask'])

def get_url_from_country(country: str) -> str:
  url = 'https://statusinvest.com.br/acoes'
  if country == 'us':
    url += '/eua'
  log('url ' + url)
  return url

def crawl_stock_price(http_client, stock_country: str, stock_name: str) -> float:
  url = get_url_from_country(stock_country)
  response = http_client.request('GET', f'{url}/{stock_name}')
  if not (response.status >= 200 and response.status < 300):
    return None

  data = BeautifulSoup(response.data, 'lxml')
  div_current = data.find_all('div', title='Valor atual do ativo')
  if div_current is None:
    return None

  for element in div_current:
    if element.find_next('strong') is not None:
      stock_price = element.find_next('strong').get_text()
      stock_price = convert_value_to_float(stock_price)
      # converting to stock price to dolar, the default curreny
      if stock_country == 'br':
        dolar_price = get_dolar_price(http_client)
        log('dolar_price ' + str(dolar_price))
        stock_price = (stock_price * dolar_price)
      return stock_price

  return None
