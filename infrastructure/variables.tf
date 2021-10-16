variable "aws_region" {
  description = "AWS region"
  type        = string
  default = "sa-east-1"
}





variable "tags" {
  type        = map(string)
  description = "Additional tags (_e.g._ { BusinessUnit : ABC })"
  default     = {}
}
