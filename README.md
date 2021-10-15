# Stocks App

```bash

docker-compose up -d mongo
docker-compose logs -f --tail 50 mongo

docker-compose exec mongo bash


docker-compose up -d --build rabbitmq
docker-compose logs -f --tail 50 rabbitmq


docker-compose up -d --build stock-api
docker-compose logs -f --tail 50 stock-api

curl --silent -X GET 'http://localhost:5050/v1/stocks/last'
curl --silent -X GET 'http://localhost:5050/v1/stocks/last/itub4'
curl --silent -X GET 'http://localhost:5050/v1/stocks/last/itsa4'
STOCKS=('itub4' 'itsa4' 'bbdc3' 'cash3' 'bbas3' 'lwsa3')


docker-compose up -d --build stock-crawler
docker-compose logs -f --tail 50 stock-crawler

```
