# Setup

To support the Python library "kubernetes" it hast to be downloaded locally and packed into a zip before uploading to aws lambda.

    cd Kubectl_Command
    pip install kubernetes --target .
    
kubernetes also needs the cluster configuration to interact with it (see [start_cluster.md](../../../kubernetes/start_cluster.md) on how to obtain it)

    cp ~/.kube/config .
	chmod a+r config
	
Then zip everything up

    zip -r9 function.zip .
    
Uploading the function package
	
	aws lambda update-function-code --function-name kubectlGet --zip-file fileb://function.zip

