
# zipping lambda function
data "archive_file" "TriggerIncidentNotification_AlertManager_mir_file" {
  type = "zip"
  source_dir = "${path.module}/lambda/TriggerIncidentNotification_AlertManager_mir"
  output_path = "${path.module}/.terraform/archive_files/TriggerIncidentNotification_AlertManager_mir.zip"
}


# function TriggerIncidentNotification_AlertManager_mir
resource "aws_lambda_function" "TriggerIncidentNotification_AlertManager_mir" {
  filename = "${data.archive_file.TriggerIncidentNotification_AlertManager_mir_file.output_path}"
  function_name = "lambda_function"
  handler = "TriggerIncidentNotification_AlertManager.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${data.archive_file.TriggerIncidentNotification_AlertManager_mir_file.output_base64sha256}"
  environment = {
    variables = {
      BearerToken = "xyz"
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.region}:${var.iam_acc_key}:alert_dispatcher"
    }
  }
}

resource "aws_lambda_permission" "TriggerIncidentNotification_AlertManager_mir" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_AlertManager_mir"]
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "TriggerIncidentNotification_AlertManager"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.BMWConnect.execution_arn}/*/*/*"
}