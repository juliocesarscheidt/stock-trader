from stock.route.base_route import BaseRoute
from stock.service.healthcheck_service import HealthcheckService


class HealthcheckRoute(BaseRoute):
    service: HealthcheckService

    def __init__(self):
        self.service = HealthcheckService()

    def get(self):
        response = self.service.get_health()
        return self.send_response(response)
