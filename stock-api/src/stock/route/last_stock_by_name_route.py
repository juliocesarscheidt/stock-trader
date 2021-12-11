from stock.route.base_route import BaseRoute
from stock.service.stock_service import StockService
from stock.common.logger import log


class LastStockByNameRoute(BaseRoute):
    service: StockService

    def __init__(self):
        self.service = StockService()

    def get(self, name: str):
        try:
            data = self.service.find_last_stock({"name": name})
            return self.send_response(data)
        except Exception as e:
            log(e)
            return self.send_response(None, 500)
