resource "aws_sns_topic" "SNSTopic1" {
  name = "SNSTopic1"
}

resource "aws_sns_topic_subscription" "AWS_SNS_Subscription_TriggerIncidentNotification_CloudWatch" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch"]
  topic_arn = "${aws_sns_topic.SNSTopic1.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.TriggerIncidentNotification_CloudWatch.arn}"
}

resource "aws_sns_topic_subscription" "AWS_SNS_Subscription_Dispatch_Alerts" {
  depends_on = ["aws_lambda_function.Dispatch_Alerts"]
  topic_arn = "${aws_sns_topic.SNSTopic1.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.TriggerIncidentNotification_CloudWatch.arn}"
}
