resource "aws_internet_gateway" "internet_gw" {
  vpc_id = aws_vpc.vpc_0.id
  tags = {
    Name = "internet_gw"
  }
  depends_on = [aws_vpc.vpc_0]
}
