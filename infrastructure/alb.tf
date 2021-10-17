resource "aws_lb" "application-lb" {
  load_balancer_type         = "application"
  name                       = "application-lb"
  internal                   = false
  enable_deletion_protection = false
  idle_timeout               = 300
  subnets                    = aws_subnet.public_subnet.*.id
  security_groups            = [aws_security_group.alb-sg.id]
  tags = {
    Name = "application-lb"
  }
  lifecycle {
    create_before_destroy = true
  }
}
