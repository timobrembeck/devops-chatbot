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
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.TriggerIncidentNotification_CloudWatch_file.output_base64sha256}"

  environment = {
    variables = {
      AlexNumber             = "+4919999999999"
      SNS_EIP_NOTIFY_ARN     = "arn:aws:sns:${var.aws_region}:${data.aws_caller_identity.current.account_id}:alert_dispatcher"
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
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.TriggerIncidentNotification_AlertManager_file.output_base64sha256}"

  environment = {
    variables = {
      BearerToken        = "xyz"
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${data.aws_caller_identity.current.account_id}:alert_dispatcher"
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

  # Generic specification
  # source_arn = "${aws_api_gateway_rest_api.alert_manager_notification_api.execution_arn}/*/*/*"
  
  # Custom specification of the source_arn 
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:rgh2w4wxk8/*/*/*"
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
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.Dispatch_Alerts_file.output_base64sha256}"

  environment = {
    variables = {
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${data.aws_caller_identity.current.account_id}:alert_to_awsconnect"
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
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
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

#--Start ReportIncident
#ReportIncident data file
data "archive_file" "ReportIncident_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/ReportIncident.zip"
}

#ReportIncident function
resource "aws_lambda_function" "ReportIncident" {
  filename         = "${data.archive_file.ReportIncident_file.output_path}"
  function_name    = "ReportIncident"
  handler          = "ReportIncident.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.ReportIncident_file.output_base64sha256}"

  environment = {
    variables = {
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${data.aws_caller_identity.current.account_id}:alert_dispatcher"
    }
  }
}
#--End ReportIncident


#--Start EscalateIncident
#EscalateIncident data file
data "archive_file" "EscalateIncident_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/EscalateIncident.zip"
}

#EscalateIncident function
resource "aws_lambda_function" "EscalateIncident" {
  filename         = "${data.archive_file.EscalateIncident_file.output_path}"
  function_name    = "EscalateIncident"
  handler          = "EscalateIncident.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.EscalateIncident_file.output_base64sha256}"

  environment = {
    variables = {
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.aws_region}:${data.aws_caller_identity.current.account_id}:alert_dispatcher"
    }
  }
}
#--End ReportIncident

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
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
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

#--Start GetIncidentByID
#GetIncidentByID data file
data "archive_file" "GetIncidentByID_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/GetIncidentByID.zip"
}

#GetIncidentByID function
resource "aws_lambda_function" "GetIncidentByID" {
  filename         = "${data.archive_file.GetIncidentByID_file.output_path}"
  function_name    = "GetIncidentByID"
  handler          = "GetIncidentByID.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.GetIncidentByID_file.output_base64sha256}"
}

#--End GetIncidentByID


#--Start Update_Incident_Status_AWSconnect
#Update_Incident_Status_AWSconnect data file
provider "aws" {
  alias = "central"
  region = "eu-central-1"
}
data "archive_file" "Update_Incident_Status_AWSconnect_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Update_Incident_Status_AWSconnect.zip"
}

#Update_Incident_Status_AWSconnect function
resource "aws_lambda_function" "Update_Incident_Status_AWSconnect" {
  provider = "aws.central"
  filename         = "${data.archive_file.Update_Incident_Status_AWSconnect_file.output_path}"
  function_name    = "Update_Incident_Status_AWSconnect"
  handler          = "Update_Incident_Status_AWSconnect.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.Update_Incident_Status_AWSconnect_file.output_base64sha256}"
}

#Update_Incident_Status_AWSconnect function permissions
resource "aws_lambda_permission" "Update_Incident_Status_AWSconnect_with_Connect" {
  depends_on    = ["aws_lambda_function.Update_Incident_Status_AWSconnect"]
  provider = "aws.central"
  statement_id  = "1"
  action        = "lambda:InvokeFunction"
  function_name = "Update_Incident_Status_AWSconnect"
  principal     = "connect.amazonaws.com"
  source_arn = "arn:aws:connect:eu-central-1:${data.aws_caller_identity.current.account_id}:instance/736d65e0-6ce5-4210-9d44-55c366ea9a16"
}

#--End Update_Incident_Status_AWSconnect

#--Start GetIncidentsByStatus
#GetIncidentsByStatus data file
data "archive_file" "GetIncidentsByStatus_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/GetIncidentsByStatus.zip"
}

#GetIncidentsByStatus function
resource "aws_lambda_function" "GetIncidentsByStatus" {
  filename         = "${data.archive_file.GetIncidentsByStatus_file.output_path}"
  function_name    = "GetIncidentsByStatus"
  handler          = "GetIncidentsByStatus.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.GetIncidentsByStatus_file.output_base64sha256}"
}
#--End GetIncidentsByStatus


#--Start GetIncidentsByPriority
#GetIncidentsByPriority data file
data "archive_file" "GetIncidentsByPriority_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/GetIncidentsByPriority.zip"
}

#GetIncidentsByPriority function
resource "aws_lambda_function" "GetIncidentsByPriority" {
  filename         = "${data.archive_file.GetIncidentsByPriority_file.output_path}"
  function_name    = "GetIncidentsByPriority"
  handler          = "GetIncidentsByPriority.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.GetIncidentsByPriority_file.output_base64sha256}"
}
#--End GetIncidentsByPriority


#--Start UpdateIncidentStatus
#UpdateIncidentStatus data file
data "archive_file" "UpdateIncidentStatus_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/UpdateIncidentStatus.zip"
}

#UpdateIncidentStatus function
resource "aws_lambda_function" "UpdateIncidentStatus" {
  filename         = "${data.archive_file.UpdateIncidentStatus_file.output_path}"
  function_name    = "UpdateIncidentStatus"
  handler          = "UpdateIncidentStatus.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.UpdateIncidentStatus_file.output_base64sha256}"
}

resource "aws_lambda_permission" "UpdateIncidentStatus_Permission" {
    depends_on = ["aws_lambda_function.UpdateIncidentStatus"]
    statement_id = "AllowExecutionFromCloseIncidentIntent"
    action = "lambda:InvokeFunction"
    function_name = "UpdateIncidentStatus"
    principal = "lex.amazonaws.com"
    source_arn = "arn:aws:lex:${var.aws_region}:${data.aws_caller_identity.current.account_id}:intent:CloseIncidentIntent:*"
}
#--End UpdateIncidentStatus




#--Start Kubectl_Command
#Kubectl_Command setup script
resource "null_resource" "Setup_Kubectl_Command" {
    provisioner "local-exec" {
        command     = "sh setup.sh"
        working_dir = "lambda_functions/Kubectl_Command"
    }
}

#Kubectl_Command data file
data "archive_file" "Kubectl_Command_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/Kubectl_Command"
  output_path = "${path.module}/.terraform/archive_files/Kubectl_Command.zip"
  depends_on  = ["null_resource.Setup_Kubectl_Command"]
}

#Kubectl_Command function
resource "aws_lambda_function" "Kubectl_Command" {
  filename         = "${data.archive_file.Kubectl_Command_file.output_path}"
  function_name    = "Kubectl_Command"
  handler          = "Kubectl_Command.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.Kubectl_Command_file.output_base64sha256}"
}

#--End Kubectl_Command



#--Start Cronjob_OutboundCall
#Cronjob_OutboundCall data file
data "archive_file" "Cronjob_OutboundCall_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Cronjob_OutboundCall.zip"
}

#Cronjob_OutboundCall function
resource "aws_lambda_function" "Cronjob_OutboundCall" {
  filename         = "${data.archive_file.Cronjob_OutboundCall_file.output_path}"
  function_name    = "Cronjob_OutboundCall"
  handler          = "Cronjob_OutboundCall.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.Cronjob_OutboundCall_file.output_base64sha256}"
}

resource "aws_cloudwatch_event_rule" "everyday_at_17" {
    name = "everyday-at-17"
    description = "Every day at 17:00"
    schedule_expression = "cron(0 17 * * ? *)"
}

resource "aws_cloudwatch_event_target" "check_everyday_at_17" {
    rule = "${aws_cloudwatch_event_rule.everyday_at_17.name}"
    target_id = "Cronjob_OutboundCall"
    arn = "${aws_lambda_function.Cronjob_OutboundCall.arn}"
}

resource "aws_lambda_permission" "Cronjob_OutboundCall_with_ScheduledEvents" {
    depends_on = ["aws_lambda_function.Cronjob_OutboundCall"]
    statement_id = "AllowExecutionFromCloudWatch-call_Cronjob_OutboundCall"
    action = "lambda:InvokeFunction"
    function_name = "Cronjob_OutboundCall"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.everyday_at_17.arn}"
}

#--End Cronjob_OutboundCall

#--Start Slack Layer

# Slack Layer data file
data "archive_file" "Slack_Lambda_Layer_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Slack_Lambda_Layer.zip"
}

# Slack Layer function
resource "aws_lambda_layer_version" "Slack_Lambda_Layer" {
  filename            = "${data.archive_file.Slack_Lambda_Layer_file.output_path}"
  layer_name          = "Slack_Lambda_Layer"
  compatible_runtimes = ["python3.6"]
  source_code_hash    = "${data.archive_file.Slack_Lambda_Layer_file.output_base64sha256}"
}

#--End Slack Layer

#--Start Create_Slack_Channel

#Create_Slack_Channel data file
data "archive_file" "Create_Slack_Channel_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Create_Slack_Channel.zip"
}

#Create_Slack_Channel function
resource "aws_lambda_function" "Create_Slack_Channel" {
  filename         = "${data.archive_file.Create_Slack_Channel_file.output_path}"
  function_name    = "Create_Slack_Channel"
  handler          = "Create_Slack_Channel.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  layers           = ["${aws_lambda_layer_version.Slack_Lambda_Layer.layer_arn}"]
  runtime          = "python3.6"
  timeout          = "200"
  source_code_hash = "${data.archive_file.Create_Slack_Channel_file.output_base64sha256}"
}

#--End Create_Slack_Channel



#--Start GetResponsibleEscalationTarget
#GetResponsibleEscalationTarget data file
data "archive_file" "GetResponsibleEscalationTarget_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/GetResponsibleEscalationTarget.zip"
}

#GetResponsibleEscalationTarget function
resource "aws_lambda_function" "GetResponsibleEscalationTarget" {
  filename         = "${data.archive_file.GetResponsibleEscalationTarget_file.output_path}"
  function_name    = "GetResponsibleEscalationTarget"
  handler          = "GetResponsibleEscalationTarget.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  runtime          = "python3.6"
  source_code_hash = "${data.archive_file.GetResponsibleEscalationTarget_file.output_base64sha256}"
}
#--End GetResponsibleEscalationTarget

#--Start Contact_Escalation_Target
#Contact_Escalation_Target data file
data "archive_file" "Contact_Escalation_Target_file" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_functions/"
  output_path = "${path.module}/.terraform/archive_files/Contact_Escalation_Target.zip"
}

#Contact_Escalation_Target function
resource "aws_lambda_function" "Contact_Escalation_Target" {
  filename         = "${data.archive_file.Contact_Escalation_Target_file.output_path}"
  function_name    = "Contact_Escalation_Target"
  handler          = "Contact_Escalation_Target.lambda_handler"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.lambda_role}"
  layers           = ["${aws_lambda_layer_version.Slack_Lambda_Layer.layer_arn}"]
  runtime          = "python3.6"
  timeout          = "600"
  source_code_hash = "${data.archive_file.Contact_Escalation_Target_file.output_base64sha256}"
}

resource "aws_lambda_permission" "Contact_Escalation_Target_Permission" {
  depends_on = ["aws_lambda_function.Contact_Escalation_Target"]
  statement_id = "AllowExecutionFromLambda-call_Contact_Escalation_Target"
  action = "lambda:InvokeFunction"
  function_name = "Contact_Escalation_Target"
  principal = "lambda.amazonaws.com"
  source_arn = "${aws_lambda_function.OutboundCall_Trigger.arn}"

}
#--End Contact_Escalation_Target
