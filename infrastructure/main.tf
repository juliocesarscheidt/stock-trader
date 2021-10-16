provider "aws" {
  region = var.aws_region
}



resource "aws_mq_configuration" "rabbitmq-configuration" {
  description    = "rabbitmq configuration"
  name           = "rabbitmq-configuration"
  engine_type    = "RabbitMQ"
  engine_version = "3.8.22"

  data = <<EOF

EOF
}

resource "aws_mq_broker" "rabbitmq" {
  broker_name = "rabbitmq"
  configuration {
    id       = aws_mq_configuration.rabbitmq-configuration.id
    revision = aws_mq_configuration.rabbitmq-configuration.latest_revision
  }
  engine_type        = "RabbitMQ"
  engine_version     = "3.8.22"
  host_instance_type = "mq.t3.micro"
  security_groups    = [aws_security_group.rabbitmq-sg.id]

  user {
    username = "root"
    password = "sPn00XcA2@#!"
  }

  depends_on = [aws_security_group.rabbitmq-sg]
}


