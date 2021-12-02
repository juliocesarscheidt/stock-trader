from bs4 import BeautifulSoup
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential

from .logger import log
from .utils import convert_value_to_float, get_dolar_price


def get_url_from_country(country: str) -> str:
    url = "https://statusinvest.com.br/acoes"
    if country == "us":
        url += "/eua"
    log("url " + url)
    return url


def crawl_stock_price(http_client, stock_country: str, stock_name: str) -> float:
    url = get_url_from_country(stock_country)
    try:
        for attempt in Retrying(stop=stop_after_attempt(3), wait=wait_exponential()):
            with attempt:
                response = http_client.request("GET", f"{url}/{stock_name}")
                if not (response.status >= 200 and response.status < 300):
                    raise Exception("[ERROR] Request error")

                data = BeautifulSoup(response.data, "lxml")
                div_current = data.find_all("div", title="Valor atual do ativo")
                if div_current is None:
                    return None

                for element in div_current:
                    if element.find_next("strong") is not None:
                        stock_price = element.find_next("strong").get_text()
                        stock_price = convert_value_to_float(stock_price)
                        # converting to stock price to dolar, the default currency
                        if stock_country == "br":
                            dolar_price = get_dolar_price(http_client)
                            log("dolar_price " + str(dolar_price))
                            stock_price = stock_price * dolar_price
                        return stock_price

                return None

    except RetryError as e:
        log(e.last_attempt.attempt_number)
        return None
    except Exception as e:
        log(e)
        raise e
