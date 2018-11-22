resource "null_resource" "test" {
  depends_on = ["aws_lambda_function.GetCurrentIncident_AWSConnect", "aws_lambda_function.Escalate_Incident"]
  provisioner "local-exec" {
    command = "python deploy_bot.py"
    working_dir = "../lex_bot"
  }
}