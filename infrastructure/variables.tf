variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "sa-east-1"
}

variable "root_domain" {
  type        = string
  description = "The root domain"
}

variable "docker_registry" {
  type        = string
  description = "Docker registry"
}

variable "cluster_name" {
  type        = string
  description = "Cluster name"
}

variable "image_version" {
  type        = string
  description = "Image version"
}

variable "rabbitmq_username" {
  type        = string
  description = "RabbitMQ username"
  default     = "rabbitmq"
}

variable "rabbitmq_password" {
  type        = string
  description = "RabbitMQ password"
}

variable "rabbitmq_engine_version" {
  type        = string
  description = "RabbitMQ engine version"
  default     = "3.8.22"
}

variable "rabbitmq_deployment_mode" {
  type        = string
  description = "RabbitMQ deployment mode"
  default     = "SINGLE_INSTANCE"
}

variable "rabbitmq_instance_type" {
  type        = string
  description = "RabbitMQ instance type"
  default     = "mq.t3.micro"
}

variable "certificate_arn" {
  type        = string
  description = "The certificate ARN"
}

# apps config
variable "app_config_stock_ui" {
  description = "Config for app stock-ui"
  type        = map(string)
  default     = {}
}
variable "app_config_stock_ui_container_port" {
  type        = number
  description = "Config for app stock-ui container ports"
}
variable "app_config_stock_ui_container_environment" {
  type        = list(any)
  description = "Config for app stock-ui container environment"
}

variable "app_config_stock_api" {
  description = "Config for app stock-api"
  type        = map(any)
  default     = {}
}
variable "app_config_stock_api_container_port" {
  type        = number
  description = "Config for app stock-api container ports"
}
variable "app_config_stock_api_container_environment" {
  type        = list(any)
  description = "Config for app stock-api container environment"
}

variable "app_config_stock_crawler" {
  description = "Config for app stock-crawler"
  type        = map(any)
  default     = {}
}
variable "app_config_stock_crawler_container_port" {
  type        = number
  description = "Config for app stock-crawler container ports"
}
variable "app_config_stock_crawler_container_environment" {
  type        = list(any)
  description = "Config for app stock-crawler container environment"
}

variable "tags" {
  type        = map(string)
  description = "Additional tags (_e.g._ { BusinessUnit : ABC })"
  default     = {}
}
