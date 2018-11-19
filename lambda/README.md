# Kubectl EKS Connection.
The typically interacts with a Kubernetes cluster through kubectl. However, that only really works for interactive commands. When you want to automate something, you need to script it. The official Python Kubernetes Lybarie is used for this purpose.
## 1. API Token for Lambda Function
The function "lambda_function.py" shows an example to interact between Lambda and a Kubernetes Cluster in eks. 
An API security token must be entered before deployment. This can be obtained as follows:
 1. Make sure that [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) are installed onm your machine.
 2. Get the token:
``` 
$ APISERVER=$(kubectl config view | grep server | cut -f 2- -d ":" | tr -d " ") 
$ TOKEN=$(kubectl describe secret $(kubectl get secrets | grep default | cut -f1 -d ' ') | grep -E '^token' | cut -f2 -d':' | tr -d '\t') 
$ curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
```
 3. Paste the token in the Lambda function
 4. Get permission for the pods.  Example use template:
```
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-list
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-list
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: ClusterRole
  name: pods-list
  apiGroup: rbac.authorization.k8s.io
```
with ``` kubectl create -f <manifest> ```
## 2. Deploy Lambda Function
Since AWS Lambda only provides standard Python packages, the Kubernetes package must be deployed in AWS. The AWS documentation ["AWS Lambda Deployment Package in Python"](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) shows how to use non-standard Python packages in aws Lambda.
