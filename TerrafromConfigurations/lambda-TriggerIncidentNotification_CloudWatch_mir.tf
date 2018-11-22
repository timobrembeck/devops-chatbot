#Zipping File TriggerIncidentNotification_CloudWatch_mir_file
data "archive_file" "TriggerIncidentNotification_CloudWatch_mir_file" {
  type = "zip"
  source_dir = "${path.module}/lambda/TriggerIncidentNotification_CloudWatch_mir"
  output_path = "${path.module}/.terraform/archive_files/TriggerIncidentNotification_CloudWatch_mir.zip"
}

#TriggerIncidentNotification_CloudWatch_mir function
resource "aws_lambda_function" "TriggerIncidentNotification_CloudWatch_mir" {
  filename = "${data.archive_file.TriggerIncidentNotification_CloudWatch_mir_file.output_path}"
  function_name = "TriggerIncidentNotification_CloudWatch_mir"
  handler = "TriggerIncidentNotification_CloudWatch_mir.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${data.archive_file.TriggerIncidentNotification_CloudWatch_mir_file.output_base64sha256}"
  environment = {
    variables = {
      AlexNumber = "+4919999999999"
      SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.region}:${var.iam_acc_key}:alert_dispatcher"
      SodNumber = "+4919999999999"
      destinationPhoneNumber = "+4919999999999"
    }
  }
}

#TriggerIncidentNotification_CloudWatch_mir function permissions
resource "aws_lambda_permission" "TriggerIncidentNotification_CloudWatch_mir_with_sns" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch_mir"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "TriggerIncidentNotification_CloudWatch_mir"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alert_from_cloudwatch_SNS.arn}"  
}
