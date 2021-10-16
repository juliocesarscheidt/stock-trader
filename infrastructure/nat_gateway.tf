resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.0.id
  tags = {
    Name = "nat_gw"
  }
  depends_on = [aws_subnet.public_subnet, aws_eip.nat_eip]
}
