#--Start TriggerIncidentNotification_CloudWatch
#TriggerIncidentNotification_CloudWatch data file
data "archive_file" "TriggerIncidentNotification_CloudWatch_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/TriggerIncidentNotification_CloudWatch.zip"
}

#TriggerIncidentNotification_CloudWatch function
resource "aws_lambda_function" "TriggerIncidentNotification_CloudWatch" {
  filename         = "${data.archive_file.TriggerIncidentNotification_CloudWatch_file.output_path}"
  function_name    = "TriggerIncidentNotification_CloudWatch"
  handler          = "TriggerIncidentNotification_CloudWatch.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.TriggerIncidentNotification_CloudWatch_file.output_base64sha256}"

  environment = {
    variables = {
      AlexNumber             = "+4919999999999"
      SNS_EIP_NOTIFY_ARN     = "arn:aws:sns:${var.aws_region}:${var.iam_acc_key}:alert_dispatcher"
      SodNumber              = "+4919999999999"
      destinationPhoneNumber = "+4919999999999"
    }
  }
}

#TriggerIncidentNotification_CloudWatch function permissions
resource "aws_lambda_permission" "TriggerIncidentNotification_CloudWatch_with_sns" {
  depends_on    = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "TriggerIncidentNotification_CloudWatch"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alert_from_cloudwatch_SNS.arn}"
}

#--End TriggerIncidentNotification_CloudWatch

#--Start TriggerIncidentNotification_AlertManager
#TriggerIncidentNotification_AlertManager data file
data "archive_file" "TriggerIncidentNotification_AlertManager_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/TriggerIncidentNotification_AlertManager.zip"
}

#TriggerIncidentNotification_AlertManager function
resource "aws_lambda_function" "TriggerIncidentNotification_AlertManager" {
  filename         = "${data.archive_file.TriggerIncidentNotification_AlertManager_file.output_path}"
  function_name    = "TriggerIncidentNotification_AlertManager"
  handler          = "TriggerIncidentNotification_AlertManager.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.TriggerIncidentNotification_AlertManager_file.output_base64sha256}"

  environment = {
    variables = {
      BearerToken        = "xyz"
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${var.iam_acc_key}:alert_dispatcher"
    }
  }
}

#TriggerIncidentNotification_AlertManager function permissions
resource "aws_lambda_permission" "TriggerIncidentNotification_AlertManager_APIGW" {
  depends_on    = ["aws_lambda_function.TriggerIncidentNotification_AlertManager"]
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "TriggerIncidentNotification_AlertManager"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.alert_manager_notification_api.execution_arn}/*/*/*"
}

#--End TriggerIncidentNotification_AlertManager

#--Start Dispatch_Alerts
#Dispatch_Alerts data file
data "archive_file" "Dispatch_Alerts_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Dispatch_Alerts.zip"
}

#Dispatch_Alerts function
resource "aws_lambda_function" "Dispatch_Alerts" {
  depends_on       = ["aws_sns_topic.alert_dispatcher_SNS"]
  filename         = "${data.archive_file.Dispatch_Alerts_file.output_path}"
  function_name    = "Dispatch_Alerts"
  handler          = "Dispatch_Alerts.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.Dispatch_Alerts_file.output_base64sha256}"

  environment = {
    variables = {
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${var.iam_acc_key}:alert_to_awsconnect"
      sodPhoneNumber     = "+4919999999999"
      odPhoneNumber_org  = "+4919999999999"
    }
  }
}

#Dispatch_Alerts function permissions
resource "aws_lambda_permission" "Dispatch_Alerts_with_sns" {
  depends_on    = ["aws_lambda_function.Dispatch_Alerts"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "Dispatch_Alerts"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alert_dispatcher_SNS.arn}"
}

#--End Dispatch_Alerts

#--Start OutboundCall_Trigger
#OutboundCall_Trigger data file
data "archive_file" "OutboundCall_Trigger_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/OutboundCall_Trigger.zip"
}

#OutboundCall_Trigger function
resource "aws_lambda_function" "OutboundCall_Trigger" {
  depends_on       = ["aws_sns_topic.alert_to_awsconnect_SNS"]
  filename         = "${data.archive_file.OutboundCall_Trigger_file.output_path}"
  function_name    = "OutboundCall_Trigger"
  handler          = "OutboundCall_Trigger.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.OutboundCall_Trigger_file.output_base64sha256}"
}

#OutboundCall_Trigger function permissions
resource "aws_lambda_permission" "OutboundCall_Trigger_with_sns" {
  depends_on    = ["aws_lambda_function.OutboundCall_Trigger"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "OutboundCall_Trigger"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alert_to_awsconnect_SNS.arn}"
}

#--Start Escalate_Incident
#Escalate_Incident data file
data "archive_file" "Escalate_Incident_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Escalate_Incident.zip"
}

#Escalate_Incident function
resource "aws_lambda_function" "Escalate_Incident" {
  filename         = "${data.archive_file.Escalate_Incident_file.output_path}"
  function_name    = "Escalate_Incident"
  handler          = "Escalate_Incident.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.Escalate_Incident_file.output_base64sha256}"

  environment = {
    variables = {
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${var.iam_acc_key}:alert_dispatcher"
    }
  }
}

#--End Escalate_Incident

#--Start GetCurrentIncident_AWSConnect
#GetCurrentIncident_AWSConnect data file
data "archive_file" "GetCurrentIncident_AWSConnect_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/GetCurrentIncident_AWSConnect.zip"
}

#GetCurrentIncident_AWSConnect function
resource "aws_lambda_function" "GetCurrentIncident_AWSConnect" {
  filename         = "${data.archive_file.GetCurrentIncident_AWSConnect_file.output_path}"
  function_name    = "GetCurrentIncident_AWSConnect"
  handler          = "GetCurrentIncident_AWSConnect.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.GetCurrentIncident_AWSConnect_file.output_base64sha256}"
}

#GetCurrentIncident_AWSConnect connect to DynamoDB
resource "aws_lambda_event_source_mapping" "aws_lambda_event_source_DDB" {
  event_source_arn  = "${aws_dynamodb_table.alert_log.stream_arn}"
  function_name     = "${aws_lambda_function.GetCurrentIncident_AWSConnect.arn}"
  starting_position = "LATEST"
}

#--End GetCurrentIncident_AWSConnect

#--Start GetIncidentWithNumber
#GetCurrentIncidentWithNumber data file
data "archive_file" "GetIncidentWithNumber_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/GetIncidentWithNumber.zip"
}

#GetIncidentWithNumber function
resource "aws_lambda_function" "GetIncidentWithNumber" {
  filename         = "${data.archive_file.GetIncidentWithNumber_file.output_path}"
  function_name    = "GetIncidentWithNumber"
  handler          = "GetIncidentWithNumber.lambda_handler"
  role             = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.GetIncidentWithNumber_file.output_base64sha256}"

  environment = {
    variables = {
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${var.iam_acc_key}:alert_dispatcher"
    }
  }
}

#--End GetIncidentWithNumber