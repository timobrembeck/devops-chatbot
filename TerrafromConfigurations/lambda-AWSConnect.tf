
data "archive_file" "GetCurrentIncident_AWSConnect_mir_file" {
  type = "zip"
  source_dir = "${path.module}/lambda/GetCurrentIncident_AWSConnect_mir"
  output_path = "${path.module}/.terraform/archive_files/GetCurrentIncident_AWSConnect_mir.zip"
}

#GetCurrentIncident_AWSConnect_mir function
resource "aws_lambda_function" "GetCurrentIncident_AWSConnect_mir" {
  filename = "${data.archive_file.GetCurrentIncident_AWSConnect_mir_file.output_path}"
  function_name = "GetCurrentIncident_AWSConnect_mir"
  handler = "GetCurrentIncident_AWSConnect_mir.lambda_handler"
  role = "arn:aws:iam::${var.iam_acc_key}:role/${var.lambda_role}"
  runtime = "python3.6"
  source_code_hash = "${data.archive_file.GetCurrentIncident_AWSConnect_mir_file.output_base64sha256}"
}

#GetCurrentIncident_AWSConnect_mir connect to DynamoDB
resource "aws_lambda_event_source_mapping" "aws_lambda_event_source_DDB" {
  event_source_arn  = "${aws_dynamodb_table.alert_log.stream_arn}"
  function_name     = "${aws_lambda_function.GetCurrentIncident_AWSConnect_mir.arn}"
  starting_position = "LATEST"
}