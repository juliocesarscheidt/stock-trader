output "mq_broker_endpoint" {
  value = local.mq_broker_endpoint
}

output "alb_record_fqdn" {
  value = aws_route53_record.alb_record.fqdn
}
