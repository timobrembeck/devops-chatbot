# Automatic Deployment of the whole infrastructure using Terraform

The alerting infrastructure needed for the devops-chatbot project can be automatically created using this terraform configuration. 

## Things to do in order to deploy the infrastructure : 
- if you want to use other AWS account than the one used by the team change the iam_acc_key variable in the variables.tf file
- navigate to the terraform folder, open a terminal and type 'terraform init'
- on the same folder path write the command 'terraform plan' on the terminal
- finally write the command 'terrform apply''

## To test the infrastructure/components: 
there is a folder called testcases, in which you can find some test data in the specific format needed by the various components. Open your AWS console, navigate to the component that you want to test and call it with the appropriate data. 

## Things needed to be implemented : 
- automatically trigger the GetCurrentIncident lambda function when the alert-log dynamoDB updates. Currently this is added manually through the dynamoDB. (seems that there is no terraform support for that, maybe write a aws-cli script and run it through terraform ?? )

- automatically deploy the Amazon Connect component which is the only component missing from the infrastructure. Connect this component to the lambda functions. (it seems that terraform does not support the Amazon Connect service, maybe write a script to create and configure this component and run it through terraform ? )
