# Automatic Deployment of the whole infrastructure using Terraform

The alerting infrastructure needed for the devops-chatbot project can be automatically created using this terraform configuration. At the moment all the components from the diagram(architecture overview) have been deployed and tested apart from the Amazon Connect component(see below).

## Things to do in order to deploy the infrastructure : 
- if you want to use other AWS account than the one used by the team change the iam_acc_key variable in the variables.tf file and your aws credentials(.config file)
- navigate to the terraform folder, open a terminal and type 'terraform init'
- on the same folder path write the command 'terraform plan' on the terminal
- finally write the command 'terrform apply''

## To test the infrastructure/components: 
there is a folder called testcases, in which you can find some test data in the specific format needed by the various components. Open your AWS console, navigate to the component that you want to test and call it with the appropriate data. 

## Things needed to be implemented : 
- automatically deploy the Amazon Connect component which is the only component missing from the infrastructure. 
- Connect this component to the lambda functions. (it seems that terraform does not support the Amazon Connect service, maybe write a script to create and configure this component and run it through terraform ? ). 
- Finally AWS does not support Amazon Connect in the eu-west-1 region(Ireland) that we are using for our current infrastructure(move everything to another region?) 
