resource "aws_mq_broker" "rabbitmq" {
  broker_name         = "rabbitmq"
  engine_type         = "RabbitMQ"
  engine_version      = var.rabbitmq_engine_version
  deployment_mode     = var.rabbitmq_deployment_mode
  publicly_accessible = true
  host_instance_type  = var.rabbitmq_instance_type
  subnet_ids          = var.rabbitmq_deployment_mode == "SINGLE_INSTANCE" ? [aws_subnet.public_subnet.0.id] : aws_subnet.public_subnet.*.id
  user {
    username = var.rabbitmq_username
    password = var.rabbitmq_password
  }
  depends_on = [aws_subnet.public_subnet]
}

provider "rabbitmq" {
  endpoint = "https://${replace(local.rabbitmq_endpoint, ":5671", "")}"
  username = var.rabbitmq_username
  password = var.rabbitmq_password
}

resource "rabbitmq_vhost" "vhost" {
  name       = "/"
  depends_on = [aws_mq_broker.rabbitmq]
}

resource "rabbitmq_permissions" "rabbitmq" {
  user  = var.rabbitmq_username
  vhost = rabbitmq_vhost.vhost.name
  permissions {
    configure = ".*"
    write     = ".*"
    read      = ".*"
  }
  depends_on = [rabbitmq_vhost.vhost]
}

resource "rabbitmq_queue" "rabbitmq-queue" {
  name  = "stocks_queue"
  vhost = rabbitmq_permissions.rabbitmq.vhost
  settings {
    durable     = true
    auto_delete = false
  }
  depends_on = [rabbitmq_permissions.rabbitmq]
}

resource "rabbitmq_exchange" "rabbitmq-exchange" {
  name  = "stocks_queue_exchange"
  vhost = rabbitmq_permissions.rabbitmq.vhost
  settings {
    type        = "direct"
    durable     = true
    auto_delete = false
  }
  depends_on = [rabbitmq_permissions.rabbitmq]
}

resource "rabbitmq_binding" "rabbitmq-binding" {
  source           = rabbitmq_exchange.rabbitmq-exchange.name
  vhost            = rabbitmq_vhost.vhost.name
  destination      = rabbitmq_queue.rabbitmq-queue.name
  destination_type = "queue"
  routing_key      = "stocks_queue"
  depends_on = [
    rabbitmq_exchange.rabbitmq-exchange,
    rabbitmq_vhost.vhost,
    rabbitmq_queue.rabbitmq-queue,
  ]
}
