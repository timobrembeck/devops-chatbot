variable "aws_region" {
  default = "eu-west-1"
}

variable "lambda_zipped_src" {
    type = "string"
    default = "lambda.zip"
}

variable "iam_acc_key" {
  type = "string"
  default = "989380504362"
}

variable "lambda_role" {
  type = "string"
  default = "lambda_sns"
}

