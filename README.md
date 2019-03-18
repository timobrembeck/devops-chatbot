# Incident management ChatBot
This project provides an infrastructure to automate the incident management of cloud-based services.
With Amazon Web Services, we use state-of-the-art technologies to implement a variety of useful tools to alert, escalate, handle and resolve incidents.
The core of our work is a chatbot which provides a human-like interface and natural language processing to enable the interaction to various web services concerning the incident management.

## Deployment

    terraform plan
    terraform apply

The alerting infrastructure needed for the devops-chatbot project can be automatically created using this terraform configuration. At the moment all the components from the diagram (architecture overview) plus the amazon lex-bot have been deployed and tested. Amazon Connect has been deployed and configured manually via the AWS console, since there is not support to automatically deploy/configure it.

- if you want to use another AWS account than the one used by the team change the iam_acc_key variable in the variables.tf file and your aws credentials(.config file)
- navigate to the terraform folder, open a terminal and type 'terraform init'
- on the same folder path write the command 'terraform plan' on the terminal
- finally write the command 'terrform apply'

## Redeploy the kubernetes config

    terraform destroy -target=null_resource.Setup_Kubectl_Command
    terraform apply -target=aws_lambda_function.Kubectl_Command    

### Terraform in development
- use -target to plan/apply single resources e.g. `terraform plan -target=aws_dynamodb_table.escalation_target`
## How to use it after deploying that
You can escalate or get the current incident via various ways. 
  - Text/Talk to the deployed 'DevOpsChatBot' lex-bot
  - Call the AWS Connect +448081649919 phone number
  - Publish an appropriate message to the 'alert_from_cloudwatch' SNS topic(see the testcases folder for example message)
  - Call the 'alert_manager_notification_api' API_GW with a POST request and appropriate request body/authentication(see the testcases folder)
