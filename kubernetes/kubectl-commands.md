# Collection of important kubectl commands that could be interasting for a bot

## System information

Resources:

all, certificatesigningrequests, clusterrolebindings, clusterroles, componentstatuses, configmaps, controllerrevisions, cronjobs, customresourcedefinition, daemonsets, deployments, endpoints, events, horizontalpodautoscalers, ingresses, jobs, limitranges, namespaces, networkpolicies, nodes, persistentvolumeclaims, persistentvolumes, poddisruptionbudgets, podpreset, pods, podsecuritypolicies, podtemplates, replicasets, replicationcontrollers, resourcequotas, rolebindings, roles, secrets, serviceaccounts, services, statefulsets, storageclasses

Verbose cluster information
- kubectl cluster-info
- kubectl cluster-info dump

Verbose resource description

- kubectl describe all

Get a resource description

- kubectl get foo

Get logs of a resource
- kubectl logs POD_NAME -c CONTAINER_NAME -p 

Get top data of a node/pod
- kubectl top node/pod foo

## System configuration

Apply a configuration to a pod
- kubectl apply -f ./pod.json

Edit a resource in editor (this is not possible from api/slack)
- kubectl edit

Autoscale a deployment
- kubectl autoscale deployment foo --min=2 --max=10

Create a resources from json
- kubectl create -f ./pod.json

Drain a node
- kubectl drain foo

Set resource labels

- kubectl label pod status=unhealthy

Expose a resources as a service
- kubectl expose 

Replace a resource by json

- kubectl replace -f ./pod.json

Rolling update pods after config change
- kubectl rolling-update foo-v1 -f foo-v2.json

Start a container instance
- kubectl run nginx --image=nginx --dry-run

Scale a replicaset
- kubectl scale --replicas=3 rs/foo

Taint a node 
- kubectl taint nodes foo dedicated=special-user:NoSchedule

Delete a resource from json
- kubectl delete foo

## Misc
Explains a resource. Could be interesting for something like a man page mode?
- kubectl explain pod/node/...


## Resources 
[https://kubernetes.io/docs/reference/kubectl/cheatsheet/](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
[https://github.com/mhausenblas/kubectl-in-action](https://github.com/mhausenblas/kubectl-in-action)
