locals {
  subnets_offset = length(data.aws_availability_zones.available_azs.names)
  public_subnets = [
    for index in range(0, local.subnets_offset) : cidrsubnet(aws_vpc.vpc_0.cidr_block, 8, index)
  ]
  private_subnets = [
    for index in range(0, local.subnets_offset) : cidrsubnet(aws_vpc.vpc_0.cidr_block, 8, index + local.subnets_offset)
  ]
  rabbitmq_endpoint  = replace(aws_mq_broker.rabbitmq.instances.*.endpoints[0][0], "amqps://", "")
  mq_broker_endpoint = "amqps://${var.rabbitmq_username}:${var.rabbitmq_password}@${local.rabbitmq_endpoint}"
}
