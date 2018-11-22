resource "aws_sns_topic" "alert_from_cloudwatch_SNS" {
  name = "alert_from_cloudwatch"
}

resource "aws_sns_topic_subscription" "AWS_SNS_Subscription_TriggerIncidentNotification_CloudWatch" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch_mir"]
  topic_arn = "${aws_sns_topic.alert_from_cloudwatch_SNS.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.TriggerIncidentNotification_CloudWatch_mir.arn}"
}

