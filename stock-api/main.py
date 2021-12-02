import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

from modules.stocks import (
    LastStocks,
    LastStocksByCountry,
    LastStockByName,
    LastStockByCountryAndName,
)
from modules.health import Health
from modules.logger import log

# application setup
app = Flask(__name__)
cors = CORS(app)
api = Api(app)

AWS_XRAY_DAEMON_ADDRESS = os.environ.get("AWS_XRAY_DAEMON_ADDRESS")

xray_recorder.configure(
    service="stock-api",
    sampling=False,
    context_missing="LOG_ERROR",
    plugins=("ECSPlugin",),
    daemon_address=AWS_XRAY_DAEMON_ADDRESS,
)
XRayMiddleware(app, xray_recorder)
patch_all()

if __name__ in "__main__":
    log("[INFO] Starting API...")
    # add endpoints
    api.add_resource(Health, "/api/v1/health")
    api.add_resource(LastStocks, "/api/v1/stocks/last")
    api.add_resource(LastStockByName, "/api/v1/stocks/last/<string:name>")
    api.add_resource(LastStocksByCountry, "/api/v1/stocks/<string:country>/last")
    api.add_resource(
        LastStockByCountryAndName, "/api/v1/stocks/<string:country>/last/<string:name>"
    )
    # start API
    app.run(host="0.0.0.0", port="5050", debug=True)
