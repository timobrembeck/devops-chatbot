# Prometheus Features
This Section descriptes, how to deploy the Testserver in a Kubernetes Cluster and monitore it via Prometheus.\\
### Prerequisites
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Setup development kubernetes cluster](https://github.com/timoludwig/devops-chatbot/tree/feature/kubernetes-demo/kubernetes) Note:The 
- Kubernetes [Kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)
### Setup
##### Testserver preparation
Build the testerserver according to the [instructions](https://github.com/timoludwig/devops-chatbot/tree/develop/testWebserver). Upload the image to dockerHub or a registry of your choice (Note: In this example dockerHub is used). 
Replace the ```Image``` variable with your docker Image Name ``` devops-chatbot/testWebserver/src/main/docker/app.yml``` (A latest version is available under p2w2/testwebserver in dockerHub)
##### Run and Deploy the testwebserver
To run the testwebserver, use:
```sh
devops-chatbot/testWebserver/src/main/docker/$ kompose up -f app.yml 
```
To delete the deployment, use:
```sh
devops-chatbot/testWebserver/src/main/docker/$ kompose down -f app.yml 
```
##### Prometheus preparation
First the devops-chatbot/prometheus/prom_server/prometheus.yml must be changed.
In the prometheus.yml file change the target "Alertmanager" to the API Gateway and the scrap target to the testserver url.
Build the prometheus Image. Upload the image to dockerHub.

##### Run and Deploy Prometheus
```sh
devops-chatbot/prometheus/prom_server/$ kompose up -f docker-compose.yml 
```
To delete the deployment, use:
```sh
devops-chatbot/prometheus/prom_server/$ kompose down -f docker-compose.yml 
```
##### Update the Prometheus Lambda Functions
Change the Enviroment variable prom_server in the prometheus_queries.py to the Prometheus server url. 
The Prometheus server url can be retrieved with ```kubectl get svc```
