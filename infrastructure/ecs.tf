resource "aws_ecs_cluster" "ecs-cluster" {
  name               = var.ecs_cluster_name
  capacity_providers = ["FARGATE_SPOT", "FARGATE"]
  default_capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
  }
  # tags = var.tags
  lifecycle {
    create_before_destroy = true
  }
}
