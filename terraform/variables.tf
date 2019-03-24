variable "aws_region" {
  default = "eu-west-1"
}

variable "lambda_role" {
  type    = "string"
  default = "lambda_sns"
}
