
#OutboundCall-Trigger_mir data file
data "archive_file" "OutboundCall-Trigger_mir_file" {
  type = "zip"
  source_dir = "${path.module}/lambda/OutboundCall-Trigger_mir"
  output_path = "${path.module}/.terraform/archive_files/OutboundCall-Trigger_mir.zip"
}

#OutboundCall-Trigger_mir function
resource "aws_lambda_function" "OutboundCall-Trigger_mir" {
  depends_on = ["aws_sns_topic.alert_to_awsconnect_SNS"]
  filename = "${data.archive_file.OutboundCall-Trigger_mir_file.output_path}"
  function_name = "OutboundCall-Trigger_mir"
  handler = "OutboundCall-Trigger_mir.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${data.archive_file.OutboundCall-Trigger_mir_file.output_base64sha256}"
}

resource "aws_lambda_permission" "OutboundCall-Trigger_mir_with_sns" {
  depends_on = ["aws_lambda_function.OutboundCall-Trigger_mir"]
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = "OutboundCall-Trigger_mir"
  principal     = "sns.amazonaws.com"
  source_arn    = "${aws_sns_topic.alert_to_awsconnect_SNS.arn}"
}

