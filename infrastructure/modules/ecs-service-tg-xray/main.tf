resource "aws_cloudwatch_log_group" "task-log-group" {
  retention_in_days = 1
  name              = "/aws/ecs/${var.app_config.name}"
}

resource "null_resource" "dependency_getter" {
  provisioner "local-exec" {
    command = "echo ${length(var.dependencies)}"
  }
}

resource "aws_ecs_task_definition" "task-definition" {
  family = "${var.app_config.name}-task-definition"
  # role for task execution, which will be used to pull the image, create log stream, start the task, etc
  execution_role_arn = var.app_config.execution_role_arn
  # role for task application, to be used by the application itself in execution time, it's optional
  task_role_arn = var.app_config.task_role_arn == "" ? aws_iam_role.ecs-task-role.arn : var.app_config.task_role_arn
  container_definitions = jsonencode([
    {
      name : var.app_config.container_name
      image : "${var.docker_registry}/${var.app_config.name}:${var.image_version}",
      portMappings = var.app_config_container_port != null ? [for port in [var.app_config_container_port] : {
        containerPort = port
        hostPort      = port
      }] : [],
      environment : length(var.app_config_container_environment) > 0 ? var.app_config_container_environment : null,
      cpu : tonumber(var.app_config.cpu),
      memory : tonumber(var.app_config.memory),
      memoryReservation : tonumber(var.app_config.memory_reservation),
      essential : true,
      logConfiguration = {
        logDriver = "awslogs",
        Options = {
          "awslogs-region"        = var.aws_region,
          "awslogs-group"         = aws_cloudwatch_log_group.task-log-group.name,
          "awslogs-stream-prefix" = "ecs",
        }
      },
      # because of awsvpc mode, we could not use links here
      # links : [
      #   "xray-daemon"
      # ],
      }, {
      name : "xray-daemon",
      image : "amazon/aws-xray-daemon:3.x",
      portMappings = [{
        containerPort = 2000
        hostPort      = 2000
        protocol      = "udp"
      }],
      cpu : 64,
      memory : 512,
      memoryReservation : 256,
    },
  ])
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  requires_compatibilities = ["FARGATE"]
  # tags = var.tags
  depends_on = [null_resource.dependency_getter]
}

resource "aws_ecs_service" "service" {
  name                               = "${var.app_config.name}-service"
  cluster                            = var.cluster_name
  task_definition                    = aws_ecs_task_definition.task-definition.arn
  scheduling_strategy                = "REPLICA"
  launch_type                        = "FARGATE"
  desired_count                      = var.app_config.desired_count
  deployment_minimum_healthy_percent = var.app_config.minimum_healthy_percent
  deployment_maximum_percent         = var.app_config.maximum_percent
  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = var.target_group_id
    container_name   = var.app_config.container_name
    container_port   = var.app_config_container_port
  }
  depends_on = [null_resource.dependency_getter]
}
