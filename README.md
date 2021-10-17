# Stocks Project

This is a project used to retrieve stocks information, from a third party website called statusinvest <https://statusinvest.com.br>, through crawling.

It is split into small services, each one with some purpose.

## Application architecture
![Architecture](./images/stocks-project-application.drawio.png)

## Up and Running

> Locally

This will start all services, then access the UI on <http://localhost:8080>

```bash
# infrastructure
docker-compose up -d --build mongo rabbitmq

# services
docker-compose up -d --build stock-crawler stock-api stock-ui
```

## Deploy on cloud

> Some notes:
For the MongoDB we are going to use Cloud MongoDB <https://cloud.mongodb.com/>, then it will not be provisioned here.

> The RabbitMQ will be the AWS MQ with interface for RabbitMQ.

## Cloud architecture

![Architecture](./images/stocks-project-cloud.drawio.png)

In order to deploy, run the following commands:

```bash
export ENV="production"
# aws settings
export AWS_ACCOUNT="000000000000"
export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION"
export AWS_BACKEND_BUCKET="backend-bucket-$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 12 | head -n1)"
# application settings
export DOCKER_REGISTRY="$AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
export CLUSTER_NAME="ecs-cluster"
export IMAGE_VERSION="0.0.1"
# rabbitmq settings
export RABBITMQ_USERNAME="rabbitmq"
export RABBITMQ_PASSWORD="$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 16 | head -n1)"
echo "RABBITMQ_PASSWORD :: ${RABBITMQ_PASSWORD}"

# login into the ECR, build the image, creates the repository (if doesn't exist) and pushes the image to the repository
make push-image

# create the backend bucket on S3 (if doesn't exist, this could take a few minutes), initializes the terraform, create the workspaces, validate and do the plan
make init

# apply the previous plan
make apply
```
