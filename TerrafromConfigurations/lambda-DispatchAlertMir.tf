#Dispatch_Alerts_mir data file
data "archive_file" "Dispatch_Alerts_mir_file" {
  type = "zip"
  source_dir = "${path.module}/lambda/Dispatch_Alerts_mir"
  output_path = "${path.module}/.terraform/archive_files/Dispatch_Alerts_mir.zip"
}
#Dispatch_Alerts_mir function
resource "aws_lambda_function" "Dispatch_Alerts_mir" {
  depends_on = ["aws_sns_topic.alert_dispatcher_SNS"]
  filename = "${data.archive_file.Dispatch_Alerts_mir_file.output_path}"
  function_name = "Dispatch_Alerts_mir"
  handler = "Dispatch_Alerts_mir.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${data.archive_file.Dispatch_Alerts_mir_file.output_base64sha256}"
  environment = {
    variables = {
        SNS_EIP_NOTIFY_ARN = "arn:aws:sns:${var.region}:${var.iam_acc_key}:alert_to_awsconnect"
        sodPhoneNumber = "+4919999999999"
        odPhoneNumber_org = "+4919999999999"
    }
  }
}
#Dispatch_Alerts_mir function permissions
resource "aws_lambda_permission" "Dispatch_Alerts_mir_with_sns" {
  depends_on = ["aws_lambda_function.Dispatch_Alerts_mir"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "Dispatch_Alerts_mir"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alert_dispatcher_SNS.arn}"
}
