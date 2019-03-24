provider "aws" {
  version = ">= 1.56.0"
  region = "${var.aws_region}"
}

data "aws_caller_identity" "current" {}