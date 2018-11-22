
resource "aws_sns_topic" "alert_to_awsconnect_SNS" {
  name = "alert_to_awsconnect"
}

resource "aws_sns_topic_subscription" "AWS_SNS_alert_to_awsconnect" {
  depends_on = ["aws_lambda_function.OutboundCall-Trigger_mir"]
  topic_arn = "${aws_sns_topic.alert_to_awsconnect_SNS.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.OutboundCall-Trigger_mir.arn}"
}
