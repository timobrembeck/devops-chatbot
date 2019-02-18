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
