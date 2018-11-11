
resource "aws_lambda_function" "TriggerIncidentNotification_CloudWatch" {
  depends_on = ["aws_sns_topic.SNSTopic1"]
  filename = "TriggerIncidentNotification_CloudWatch.zip"
  function_name = "TriggerIncidentNotification_CloudWatch"
  handler = "TriggerIncidentNotification_CloudWatch.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("TriggerIncidentNotification_CloudWatch.zip"))}"
  environment = {
    variables = {
      AlexNumber = "+4919999999999"
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:eu-central-1:583726959404:alert_to_awsconnect"
      SodNumber = "+4919999999999"
      destinationPhoneNumber = "+4919999999999"
    }
  }
}

resource "aws_lambda_permission" "TriggerIncidentNotification_CloudWatch_with_sns" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "TriggerIncidentNotification_CloudWatch"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.SNSTopic1.arn}"
}




resource "aws_lambda_function" "TriggerIncidentNotification_AlertManager" {
  filename = "TriggerIncidentNotification_AlertManager.zip"
  function_name = "TriggerIncidentNotification_AlertManager"
  handler = "TriggerIncidentNotification_AlertManager.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("TriggerIncidentNotification_AlertManager.zip"))}"
  environment = {
    variables = {
      BearerToken = "xyz"
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:eu-central-1:583726959404:alert_dispatcher"
    }
  }
}

resource "aws_lambda_permission" "TriggerIncidentNotification_AlertManager_APIGW" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_AlertManager"]
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "TriggerIncidentNotification_AlertManager"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.alert_manager_notification_api.execution_arn}/*/*/*"
}





resource "aws_lambda_function" "Dispatch_Alerts" {
  depends_on = ["aws_sns_topic.SNSTopic1"]
  filename = "Dispatch_Alerts.zip"
  function_name = "Dispatch_Alerts"
  handler = "Dispatch_Alerts.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("Dispatch_Alerts.zip"))}"
  environment = {
    variables = {
        sodPhoneNumber = "+4919999999999"
        odPhoneNumber_org = "+4919999999999"
    }
  }
}

resource "aws_lambda_permission" "Dispatch_Alerts_with_sns" {
  depends_on = ["aws_lambda_function.Dispatch_Alerts"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "Dispatch_Alerts"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.SNSTopic1.arn}"
}







resource "aws_lambda_function" "GetCurrentIncident_AWSConnect" {
  depends_on = ["aws_dynamodb_table.alert-log"]
  filename = "GetCurrentIncident_AWSConnect.zip"
  function_name = "GetCurrentIncident_AWSConnect"
  handler = "GetCurrentIncident_AWSConnect.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("GetCurrentIncident_AWSConnect.zip"))}"
}



resource "aws_lambda_function" "OutboundCall_Trigger" {
  depends_on = ["aws_sns_topic.SNSTopic1"]
  filename = "OutboundCall_Trigger.zip"
  function_name = "OutboundCall_Trigger"
  handler = "OutboundCall_Trigger.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("OutboundCall_Trigger.zip"))}"
}

resource "aws_lambda_permission" "OutboundCall_Trigger_with_sns" {
  depends_on = ["aws_lambda_function.OutboundCall_Trigger"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "OutboundCall_Trigger"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.SNSTopic1.arn}"
}



resource "aws_lambda_function" "ResolveCurrentIncident_AWSConnect" {
  depends_on = ["aws_dynamodb_table.alert-log"]
  filename = "ResolveCurrentIncident_AWSConnect.zip"
  function_name = "ResolveCurrentIncident_AWSConnect"
  handler = "ResolveCurrentIncident_AWSConnect.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("ResolveCurrentIncident_AWSConnect.zip"))}"
}




resource "aws_lambda_function" "Escalate_Incident" {
  depends_on = ["aws_sns_topic.SNSTopic1"]
  filename = "Escalate_Incident.zip"
  function_name = "Escalate_Incident"
  handler = "Escalate_Incident.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${base64sha256(file("Escalate_Incident.zip"))}"
}
