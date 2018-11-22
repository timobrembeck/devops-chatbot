# boiler plate code for AWS api name
resource "aws_api_gateway_rest_api" "BMWConnect" {
  name        = "BMWConnectApplication"
  description = "BMWConnectApplication Using terraform on AWS"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = "${aws_api_gateway_rest_api.BMWConnect.id}"
  parent_id   = "${aws_api_gateway_rest_api.BMWConnect.root_resource_id}"
  path_part   = "{proxy+}"
}
#setting authorization of api
resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = "${aws_api_gateway_rest_api.BMWConnect.id}"
  resource_id   = "${aws_api_gateway_resource.proxy.id}"
  http_method   = "ANY"
  authorization = "NONE"
}
# connections of api to lambda upon POST
resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = "${aws_api_gateway_rest_api.BMWConnect.id}"
  resource_id = "${aws_api_gateway_method.proxy.resource_id}"
  http_method = "${aws_api_gateway_method.proxy.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.TriggerIncidentNotification_AlertManager_mir.invoke_arn}"

}

resource "aws_api_gateway_method" "proxy_root" {
  rest_api_id   = "${aws_api_gateway_rest_api.BMWConnect.id}"
  resource_id   = "${aws_api_gateway_rest_api.BMWConnect.root_resource_id}"
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_root" {
  rest_api_id = "${aws_api_gateway_rest_api.BMWConnect.id}"
  resource_id = "${aws_api_gateway_method.proxy_root.resource_id}"
  http_method = "${aws_api_gateway_method.proxy_root.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.TriggerIncidentNotification_AlertManager_mir.invoke_arn}"
}

#aws_api_gateway_deployment in production/test
resource "aws_api_gateway_deployment" "BMWConnect" {
  depends_on = [
    "aws_api_gateway_integration.lambda",
    "aws_api_gateway_integration.lambda_root",
  ]

  rest_api_id = "${aws_api_gateway_rest_api.BMWConnect.id}"
  stage_name  = "BMW API IN TEST"
}