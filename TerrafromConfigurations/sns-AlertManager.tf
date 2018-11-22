
resource "aws_sns_topic" "alert_dispatcher_SNS" {
  name = "alert_dispatcher"
}

resource "aws_sns_topic_subscription" "AWS_SNS_Dispatch_One" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_AlertManager_mir"]
  topic_arn = "${aws_sns_topic.alert_dispatcher_SNS.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.Dispatch_Alerts_mir.arn}"
}

resource "aws_sns_topic_subscription" "AWS_SNS_Dispatch_Two" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_AlertManager_mir"]
  topic_arn = "${aws_sns_topic.alert_dispatcher_SNS.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.Dispatch_Alerts_mir.arn}"
}
