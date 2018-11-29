#--Start alert_from_cloudwatch
#alert_from_cloudwatch SNS topic
resource "aws_sns_topic" "alert_from_cloudwatch_SNS" {
  name = "alert_from_cloudwatch"
}

#alert_from_cloudwatch subscription to TriggerIncidentNotification_CloudWatch lambda function
resource "aws_sns_topic_subscription" "AWS_SNS_Subscription_TriggerIncidentNotification_CloudWatch" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch"]
  topic_arn  = "${aws_sns_topic.alert_from_cloudwatch_SNS.arn}"
  protocol   = "lambda"
  endpoint   = "${aws_lambda_function.TriggerIncidentNotification_CloudWatch.arn}"
}

#--End alert_from_cloudwatch

#--Start alert_dispatcher
#alert_dispatcher SNS topic
resource "aws_sns_topic" "alert_dispatcher_SNS" {
  name = "alert_dispatcher"
}

#alert_dispatcher subscription to TriggerIncidentNotification_CloudWatch lambda function
resource "aws_sns_topic_subscription" "AWS_SNS_Dispatch_Alerts1" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_CloudWatch"]
  topic_arn  = "${aws_sns_topic.alert_dispatcher_SNS.arn}"
  protocol   = "lambda"
  endpoint   = "${aws_lambda_function.Dispatch_Alerts.arn}"
}

#alert_dispatcher subscription to TriggerIncidentNotification_CloudWatch lambda function
resource "aws_sns_topic_subscription" "AWS_SNS_Dispatch_Alerts2" {
  depends_on = ["aws_lambda_function.TriggerIncidentNotification_AlertManager"]
  topic_arn  = "${aws_sns_topic.alert_dispatcher_SNS.arn}"
  protocol   = "lambda"
  endpoint   = "${aws_lambda_function.Dispatch_Alerts.arn}"
}

#--End alert_dispatcher

#--Start alert_to_awsconnect
#alert_to_awsconnect SNS topic
resource "aws_sns_topic" "alert_to_awsconnect_SNS" {
  name = "alert_to_awsconnect"
}

#alert_to_awsconnect subscription to OutboundCall_Trigger lambda function
resource "aws_sns_topic_subscription" "AWS_SNS_alert_to_awsconnect" {
  depends_on = ["aws_lambda_function.OutboundCall_Trigger"]
  topic_arn  = "${aws_sns_topic.alert_to_awsconnect_SNS.arn}"
  protocol   = "lambda"
  endpoint   = "${aws_lambda_function.OutboundCall_Trigger.arn}"
}

#--End alert_to_awsconnect

