resource "null_resource" "test" {
  depends_on = [
    "aws_lambda_function.GetCurrentIncident_AWSConnect",
    "aws_lambda_function.Escalate_Incident",
  ]

  provisioner "local-exec" {
    command     = "python deploy.py create"
    working_dir = "../lex_bot"
  }

  provisioner "local-exec" {
    when        = "destroy"
    command     = "python deploy.py destroy"
    working_dir = "../lex_bot"
  }
}
