# this is a sample file
aws_region        = "sa-east-1"
root_domain       = "domain.com.br"
docker_registry   = "000000000000.dkr.ecr.sa-east-1.amazonaws.com"
cluster_name      = "ecs-cluster"
certificate_arn   = "arn:aws:acm:sa-east-1:000000000000:certificate/00000000-0000-0000-0000-000000000000"
image_version     = "0.0.1"
rabbitmq_username = "rabbitmq"
rabbitmq_password = ""
# e.g. 000000000000.dkr.ecr.sa-east-1.amazonaws.com/stock-ui:0.0.1
app_config_stock_ui = {
  "name"                    = "stock-ui"
  "container_name"          = "stock-ui"
  "execution_role_arn"      = "arn:aws:iam::000000000000:role/AmazonECSTaskExecutionRole"
  "task_role_arn"           = ""
  "cpu"                     = "512"
  "memory"                  = "1024"
  "memory_reservation"      = "256"
  "desired_count"           = "1"
  "minimum_healthy_percent" = "0"
  "maximum_percent"         = "100"
}
app_config_stock_ui_container_port = 80
app_config_stock_ui_container_environment = [
  { "name" : "NODE_ENV", "value" : "production" },
]
# e.g. 000000000000.dkr.ecr.sa-east-1.amazonaws.com/stock-api:0.0.1
app_config_stock_api = {
  "name"                    = "stock-api"
  "container_name"          = "stock-api"
  "execution_role_arn"      = "arn:aws:iam::000000000000:role/AmazonECSTaskExecutionRole"
  "task_role_arn"           = ""
  "cpu"                     = "512"
  "memory"                  = "1024"
  "memory_reservation"      = "256"
  "desired_count"           = "1"
  "minimum_healthy_percent" = "0"
  "maximum_percent"         = "100"
}
app_config_stock_api_container_port = 5050
app_config_stock_api_container_environment = [
  { "name" : "MONGO_URI", "value" : "" }, # this variable should be filled in
  { "name" : "RABBITMQ_EXCHANGE", "value" : "stocks_queue_exchange" },
  { "name" : "RABBITMQ_ROUTING_KEY", "value" : "stocks_queue" },
  { "name" : "FLASK_ENV", "value" : "production" },
  { "name" : "AWS_XRAY_DAEMON_ADDRESS", "value" : "127.0.0.1:2000" },
]
# e.g. 000000000000.dkr.ecr.sa-east-1.amazonaws.com/stock-crawler:0.0.1
app_config_stock_crawler = {
  "name"                    = "stock-crawler"
  "container_name"          = "stock-crawler"
  "execution_role_arn"      = "arn:aws:iam::000000000000:role/AmazonECSTaskExecutionRole"
  "task_role_arn"           = ""
  "cpu"                     = "512"
  "memory"                  = "1024"
  "memory_reservation"      = "256"
  "desired_count"           = "1"
  "minimum_healthy_percent" = "0"
  "maximum_percent"         = "100"
}
app_config_stock_crawler_container_port = null
app_config_stock_crawler_container_environment = [
  { "name" : "MONGO_URI", "value" : "" }, # this variable should be filled in
  { "name" : "RABBITMQ_QUEUE", "value" : "stocks_queue" },
]
tags = {
  "ENVIRONMENT" = "DEVELOPMENT"
  "PROVIDER"    = "TERRAFORM"
}
