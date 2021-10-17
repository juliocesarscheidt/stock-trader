resource "aws_ecs_cluster" "ecs-cluster" {
  name               = var.cluster_name
  capacity_providers = ["FARGATE_SPOT", "FARGATE"]
  default_capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
  }
  # tags = var.tags
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_service_discovery_private_dns_namespace" "private-dns-namespace" {
  name        = "${aws_ecs_cluster.ecs-cluster.name}.local"
  description = "ECS Namespace for Service Discovery"
  vpc         = aws_vpc.vpc_0.id
  tags = {
    Name = "${aws_ecs_cluster.ecs-cluster.name}.local"
  }
  depends_on = [aws_ecs_cluster.ecs-cluster]
}

resource "aws_service_discovery_service" "service-discovery" {
  name = "service-discovery"
  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.private-dns-namespace.id
    dns_records {
      ttl  = 10
      type = "A"
    }
    routing_policy = "MULTIVALUE"
  }
  tags = {
    Name = "service-discovery"
  }
  depends_on = [aws_ecs_cluster.ecs-cluster]
}

module "stock-ui" {
  source = "./modules/ecs-service-tg"

  aws_region                       = var.aws_region
  docker_registry                  = var.docker_registry
  cluster_name                     = var.cluster_name
  image_version                    = var.image_version
  service_discovery_arn            = aws_service_discovery_service.service-discovery.arn
  subnet_ids                       = aws_subnet.private_subnet.*.id
  security_group_ids               = [aws_security_group.stock-ui-sg.id]
  target_group_id                  = aws_alb_target_group.stock-ui-tg.id
  app_config                       = var.app_config_stock_ui
  app_config_container_port        = var.app_config_stock_ui_container_port
  app_config_container_environment = var.app_config_stock_ui_container_environment
  tags                             = var.tags
}

module "stock-api" {
  source = "./modules/ecs-service-tg"

  aws_region                       = var.aws_region
  docker_registry                  = var.docker_registry
  cluster_name                     = var.cluster_name
  image_version                    = var.image_version
  service_discovery_arn            = aws_service_discovery_service.service-discovery.arn
  subnet_ids                       = aws_subnet.private_subnet.*.id
  security_group_ids               = [aws_security_group.stock-api-sg.id]
  target_group_id                  = aws_alb_target_group.stock-api-tg.id
  app_config                       = var.app_config_stock_api
  app_config_container_port        = var.app_config_stock_api_container_port
  app_config_container_environment = concat(var.app_config_stock_api_container_environment, [{ "name" : "RABBITMQ_URI", "value" : local.mq_broker_endpoint }])
  tags                             = var.tags
}

module "stock-crawler" {
  source = "./modules/ecs-service"

  aws_region                       = var.aws_region
  docker_registry                  = var.docker_registry
  cluster_name                     = var.cluster_name
  image_version                    = var.image_version
  service_discovery_arn            = aws_service_discovery_service.service-discovery.arn
  subnet_ids                       = aws_subnet.private_subnet.*.id
  security_group_ids               = [aws_security_group.stock-crawler-sg.id]
  app_config                       = var.app_config_stock_crawler
  app_config_container_port        = var.app_config_stock_crawler_container_port
  app_config_container_environment = concat(var.app_config_stock_crawler_container_environment, [{ "name" : "RABBITMQ_URI", "value" : local.mq_broker_endpoint }])
  tags                             = var.tags
}
