# How kubernetes works

## Architecture

* Kubernetes runs docker containers across multiple clusters
* You need to write jobs that creates the pods to execute the work

### Pods vs Jobs
* You write jobs that create pods
  * A job can create multiple pods (1-to-many)
  * A job keeps running until it is complete
  * If a job is not complete it will continue recreating pods until it is complete (or another condition)
 
### kubectl vs k9s
* kubectl is how we control kubernetes
* k9s is just a UI wrapper around kubectl
* You usually want to use kubectl to kill pods / get pods etc in bulk using a programming language & logic
  
