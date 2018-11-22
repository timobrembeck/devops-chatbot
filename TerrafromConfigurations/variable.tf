variable "access_key" {
  default = ""
}
variable "secret_key" {
  default = ""
}
variable "region" {
  default = "eu-west-1"
}

variable "iam_acc_key" {
  type = "string"
  default = "746022503515"
}

variable "lambda_role" {
  type = "string"
  default = "lambda_sns"
}
