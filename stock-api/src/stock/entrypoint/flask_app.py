from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

from stock.config import get_xray_config
from stock.route.healthcheck_route import HealthcheckRoute
from stock.route.last_stocks_route import LastStocksRoute
from stock.route.last_stocks_by_country_route import LastStocksByCountryRoute
from stock.route.last_stock_by_country_name_route import LastStockByCountryNameRoute
from stock.route.last_stock_by_name_route import LastStockByNameRoute

# application setup
app = Flask(__name__)
cors = CORS(app)
api = Api(app)

xray_recorder.configure(
    service="stock-api",
    sampling=False,
    context_missing="LOG_ERROR",
    plugins=("ECSPlugin",),
    daemon_address=get_xray_config()["address"],
)
XRayMiddleware(app, xray_recorder)
patch_all()

api.add_resource(HealthcheckRoute, "/api/v1/health")
api.add_resource(LastStocksRoute, "/api/v1/stocks/last")
api.add_resource(LastStockByNameRoute, "/api/v1/stocks/last/<string:name>")
api.add_resource(LastStocksByCountryRoute, "/api/v1/stocks/<string:country>/last")
api.add_resource(
    LastStockByCountryNameRoute, "/api/v1/stocks/<string:country>/last/<string:name>"
)

# start API (done by flask run command on entrypoint)
# app.run(host="0.0.0.0", port="5050", debug=True)
