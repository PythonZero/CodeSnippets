# Connecting to EKS (Elastic Kubernetes Cluster)

1) Connect to the eks cluster 
```bash
aws eks update-kubeconfig --name <clustername> --region <region>
```
   * this will add the config to your `kubectl` config
   * check by running `kubectl config view`
   * This will now let you connect to the cluster (via k9s), and access resources in the cluster (e.g. helm)
   
2) Run `k9s`
   * Install `brew install k9s` if you don't have it
   * This should now allow you to connect to the EKS cluster

3) You should now also have access to the helm charts
   * check by running `helm get values airflow -n airflow`
   * replacing `airflow` with your helm chart name, and `-n airflow` with your namespace

