

data "archive_file" "Escalate_Incident_To_mir_file" {
  type = "zip"
  source_dir = "${path.module}/lambda/Escalate_Incident_To_mir"
  output_path = "${path.module}/.terraform/archive_files/Escalate_Incident_To_mir.zip"
}

resource "aws_lambda_function" "Escalate_Incident_To_mir" {
  filename = "${data.archive_file.Escalate_Incident_To_mir_file.output_path}"
  function_name = "Escalate_Incident_To_mir"
  handler = "Escalate_Incident_To_mir.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${data.archive_file.Escalate_Incident_To_mir_file.output_base64sha256}"
  environment = {
    variables = {
        SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.region}:${var.iam_acc_key}:alert_dispatcher"
    }
  }
}
