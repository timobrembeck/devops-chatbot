# Automatic Deployment of the whole infrastructure using Terraform

What has been implemented : 
	
	- API Gateway which triggers TriggerIncidentNotification_AlertManager lambda function

	- SNS topic which triggers TriggerIncidentNotification_CloudWatch

	- TriggerIncidentNotification_AlertManager lambda function gets triggered from API_GW, checks for authentication(Bearer token), formats the data and publish to SNS

	- TriggerIncidentNotification_CloudWatch lambda function gets triggered from the SNS topic, formats the data and publish back to SNS

	- DynamoDB table alert-log, which holds the messages

	- Dispatch_Alerts lambda function that publish to SNS 

	- OutboundCall_Trigger lambda function(See the Questions/Concerns below)

	- Escalate_Incident lambda function which escalates events to SNS topic

	- GetCurrentIncident_AWSConnect lambda function which queries DynamoDB and finds the last incident


Questions/Concerns: 

	- OutboundCall_Trigger Function does not return anything and has a strange function call in the end -> start_outbound_voice_contact

	- Terraform does not seem to support AWS connect

	- ResolveCurrentIncident_AWSConnect is not displayed on the architecture diagram


