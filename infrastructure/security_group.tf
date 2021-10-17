resource "aws_security_group" "stock-ui-sg" {
  vpc_id = aws_vpc.vpc_0.id
  name   = "stock-ui-sg"
  # outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # inbound rules
  ingress {
    from_port       = var.app_config_stock_ui_container_port
    to_port         = var.app_config_stock_ui_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb-sg.id]
  }
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_security_group.alb-sg]
}

resource "aws_security_group" "stock-api-sg" {
  vpc_id = aws_vpc.vpc_0.id
  name   = "stock-api-sg"
  # outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # inbound rules
  ingress {
    from_port       = var.app_config_stock_api_container_port
    to_port         = var.app_config_stock_api_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb-sg.id]
  }
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_security_group.alb-sg]
}

resource "aws_security_group" "stock-crawler-sg" {
  vpc_id = aws_vpc.vpc_0.id
  name   = "stock-crawler-sg"
  # outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # inbound rules
  # ingress {}
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_security_group.alb-sg]
}

resource "aws_security_group" "alb-sg" {
  vpc_id = aws_vpc.vpc_0.id
  name   = "alb-sg"
  # outbound rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # inbound rules
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  lifecycle {
    create_before_destroy = true
  }
}

# resource "aws_security_group" "rabbitmq-sg" {
#   vpc_id = aws_vpc.vpc_0.id
#   name   = "rabbitmq-sg"
#   # outbound rules
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   # inbound rules
#   ingress {
#     from_port   = 5671
#     to_port     = 5671
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   ingress {
#     from_port   = 443
#     to_port     = 443
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   lifecycle {
#     create_before_destroy = true
#   }
# }
