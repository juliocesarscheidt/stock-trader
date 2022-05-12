# Docker Commands

```bash

# mongo
docker-compose up -d mongo
docker-compose logs -f --tail 50 mongo

docker-compose exec mongo bash

# rabbitmq
docker-compose up -d --build rabbitmq
docker-compose logs -f --tail 50 rabbitmq

# crawler
docker-compose up -d --build stock-crawler
docker-compose logs -f --tail 50 stock-crawler

# API
docker-compose up -d --build stock-api
docker-compose logs -f --tail 50 stock-api

# try out API
curl --silent -X GET 'http://localhost:5050/api/stocks/br/last' | jq -r '.'

STOCKS=('itub4' 'itsa4' 'bbdc3' 'cash3' 'bbas3' 'lwsa3' 'lame4' 'ciel3' 'embr3')
for STOCK in "${STOCKS[@]}"; do
  curl --silent -X GET "http://localhost:5050/api/stocks/br/last/${STOCK}" | jq -r '.'
done

curl --silent -X GET 'http://localhost:5050/api/stocks/br/last/itub4' | jq -r '.'
curl --silent -X GET 'http://localhost:5050/api/stocks/br/last/itsa4' | jq -r '.'

# ui
docker-compose up -d --build stock-ui
docker-compose logs -f --tail 50 stock-ui

```
