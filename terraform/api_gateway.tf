resource "aws_api_gateway_rest_api" "alert_manager_notification_api" {
  name        = "alert_manager_notification_api"
  description = "The Alert Manager Notification API to trigger the TriggerIncidentNotification_Alert"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = "${aws_api_gateway_rest_api.alert_manager_notification_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.alert_manager_notification_api.root_resource_id}"
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = "${aws_api_gateway_rest_api.alert_manager_notification_api.id}"
  resource_id   = "${aws_api_gateway_resource.proxy.id}"
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = "${aws_api_gateway_rest_api.alert_manager_notification_api.id}"
  resource_id = "${aws_api_gateway_method.proxy.resource_id}"
  http_method = "${aws_api_gateway_method.proxy.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.TriggerIncidentNotification_CloudWatch.invoke_arn}"
}


resource "aws_api_gateway_method" "proxy_root" {
  rest_api_id   = "${aws_api_gateway_rest_api.alert_manager_notification_api.id}"
  resource_id   = "${aws_api_gateway_rest_api.alert_manager_notification_api.root_resource_id}"
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_root" {
  rest_api_id = "${aws_api_gateway_rest_api.alert_manager_notification_api.id}"
  resource_id = "${aws_api_gateway_method.proxy_root.resource_id}"
  http_method = "${aws_api_gateway_method.proxy_root.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.TriggerIncidentNotification_CloudWatch.invoke_arn}"
}


resource "aws_api_gateway_deployment" "alert_manager_notification_api" {
  depends_on = [
    "aws_api_gateway_integration.lambda",
    "aws_api_gateway_integration.lambda_root",
  ]

  rest_api_id = "${aws_api_gateway_rest_api.alert_manager_notification_api.id}"
  stage_name  = "alert_manager_notification_api_stage_name"
}

