> :warning: This project is no longer maintained

# Incident management ChatBot
This project provides an infrastructure to automate the incident management of cloud-based services.
With Amazon Web Services, we use state-of-the-art technologies to implement a variety of useful tools to alert, escalate, handle and resolve incidents.
The core of our work is a chatbot which provides a human-like interface and natural language processing to enable the interaction to various web services concerning the incident management.

## Deployment

    terraform plan
    terraform apply

The alerting infrastructure needed for the devops-chatbot project can be automatically created using this terraform configuration. At the moment all the components from the diagram (architecture overview) plus the amazon lex-bot have been deployed and tested. Amazon Connect has been deployed and configured manually via the AWS console, since there is not support to automatically deploy/configure it.

### Deploy only specific components
Use -target to plan/apply single resources e.g.:
`terraform plan -target=aws_dynamodb_table.escalation_target`

Redeploy the kubernetes config:

    terraform destroy -target=null_resource.Setup_Kubectl_Command
    terraform apply -target=aws_lambda_function.Kubectl_Command    

## Usage
You can escalate or get the current incident via various ways. 
  - Text/Talk to the deployed 'DevOpsChatBot' lex-bot
  - Call the phone number configured in AWS Connect
  - Publish an appropriate message to the 'alert_from_cloudwatch' SNS topic(see the testcases folder for example message)
  - Call the 'alert_manager_notification_api' API_GW with a POST request and appropriate request body/authentication(see the testcases folder)
