resource "null_resource" "Lex_Bot" {
  depends_on = [
    "aws_lambda_function.GetCurrentIncident_AWSConnect",
    "aws_lambda_function.ReportIncident",
    "aws_lambda_function.EscalateIncident",
    "aws_lambda_function.GetIncidentByID",
    "aws_lambda_function.GetIncidentsByPriority",
    "aws_lambda_function.GetIncidentsByStatus",
    "aws_lambda_function.UpdateIncidentStatus",
    "aws_lambda_function.Kubectl_Command",
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
