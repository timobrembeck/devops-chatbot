# Lambda functions to interact with a K8 Cluster via kubectl

This readme describes how to deploy minimal kubectl lambda wrapper on aws lambda.
You can us the example data at the end of the `lambda_functions/kubectlGet.py` to test the bot local or in aws lambda.
A minimal bot called `kubectlBot` is implementing the lambda function fot fullfilment.


## Setup development kubernetes cluster

Export some regularly used variables in your shell

	export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
	export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
	export NAME=fog-chatbot-dev.k8s.local
	export NODE_SIZE=${NODE_SIZE:-t2.micro}
	export MASTER_SIZE=${MASTER_SIZE:-t2.micro}
	export ZONES=${ZONES:-"eu-west-1a"}
	export KOPS_STATE_STORE=s3://fog-chatbot-dev-kcluster-state-store

Create a minimal cluster configuration
If this fails the cluster is probably already created and the current config is stored in the `KOP_STATE_STORE` on S3 (go to next step)

	kops create cluster $NAME \
	--node-count 1 \
	--zones $ZONES \
	--node-size $NODE_SIZE \
	--master-size $MASTER_SIZE \
	--master-zones $ZONES

If the config already exists and the cluster is running you can import the current kubectl config from the S3 state store via

	kops export kubecfg ${NAME}

If the cluster is not running yet run update to start it:

	kops update cluster $NAME
	kops update cluster $NAME --yes

Please don't forget to shutdown the cluster after using

    kops delete cluster --name $NAME
    kops delete cluster --name $NAME

## Building / Deploying the functions

### Creating the file structure

	cd lambda_functions
	pip install kubernetes --target .
	
	
**This is a `hack` used in development to add the kubectl config to the lambda environment and enable easy credential access**
	
	cp ~/.kube/config .
	chmod a+r config
    
### Building the zip
	zip -r9 function.zip .

### Uploading the function package
	
	aws lambda update-function-code --function-name kubectlGet --zip-file fileb://function.zip


### Redeploying after changing the function

    zip -g function.zip kubectlGet.py
    aws lambda update-function-code --function-name kubectlGet --zip-file fileb://function.zip
    
## Deleting the cluster

    kops delete cluster --name $NAME
    kops delete cluster --name $NAME --yes
