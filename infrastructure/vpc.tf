resource "aws_vpc" "vpc_0" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  enable_classiclink   = "false"
  tags = {
    Name = "vpc_0"
  }
}



data "aws_availability_zones" "available_azs" {
  state = "available"
}


locals {
  subnets_offset = length(data.aws_availability_zones.available_azs.names)
  public_subnets = [
    for index in range(0, local.subnets_offset) : cidrsubnet(aws_vpc.vpc_0.cidr_block, 8, index)
  ]
  private_subnets = [
    for index in range(0, local.subnets_offset) : cidrsubnet(aws_vpc.vpc_0.cidr_block, 8, index + local.subnets_offset)
  ]
}


######## PUBLIC SUBNET ########
resource "aws_subnet" "public_subnet" {
  count                   = local.subnets_offset
  cidr_block              = local.public_subnets[count.index]
  availability_zone       = data.aws_availability_zones.available_azs.names[count.index]
  vpc_id                  = aws_vpc.vpc_0.id
  map_public_ip_on_launch = true
  tags = {
    Name = "public_subnet_${count.index}"
  }
  depends_on = [aws_vpc.vpc_0]
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc_0.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gw.id
  }
  tags = {
    Name = "public_route_table"
  }
  depends_on = [aws_internet_gateway.internet_gw]
}

resource "aws_route_table_association" "assoc_route_public" {
  count          = local.subnets_offset
  subnet_id      = element(aws_subnet.public_subnet.*.id, count.index)
  route_table_id = aws_route_table.public_route_table.id
  depends_on     = [aws_subnet.public_subnet, aws_route_table.public_route_table]
}

# change the main route
resource "aws_main_route_table_association" "assoc_main_route" {
  vpc_id         = aws_vpc.vpc_0.id
  route_table_id = aws_route_table.public_route_table.id
  depends_on     = [aws_vpc.vpc_0, aws_route_table.public_route_table]
}

######## PRIVATE SUBNET ########
resource "aws_subnet" "private_subnet" {
  count                   = local.subnets_offset
  cidr_block              = local.private_subnets[count.index]
  availability_zone       = data.aws_availability_zones.available_azs.names[count.index]
  vpc_id                  = aws_vpc.vpc_0.id
  map_public_ip_on_launch = false
  tags = {
    Name = "private_subnet_${count.index}"
  }
  depends_on = [aws_vpc.vpc_0]
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc_0.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw.id
  }
  tags = {
    Name = "private_route_table"
  }
  depends_on = [aws_nat_gateway.nat_gw]
}

resource "aws_route_table_association" "assoc_route_private" {
  count          = local.subnets_offset
  subnet_id      = element(aws_subnet.private_subnet.*.id, count.index)
  route_table_id = aws_route_table.private_route_table.id
  depends_on     = [aws_subnet.private_subnet, aws_route_table.private_route_table]
}


