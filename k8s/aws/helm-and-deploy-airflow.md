# Updating helm charts

1. Get existing helm chart 

```
helm get values airflow -n airflow
```

2. Save these values somewhere (e.g. `/home/user/PROJECTS/values-config/my-chart.yaml` )

3. Make any changes to the charts (e.g. update the sql database)

4. SUPER IMPORTANT - change directory INTO the folder with the Charts.yaml file, e.g.

```
cd /home/user/PROJECTS/helm-charts/airflow-deployment
```

5. Deploy the updated helm charts 
```
helm upgrade --install airflow . --namespace my-namespace-prod1 --values /home/user/PROJECTS/values-config/my-chart.yaml  --set environment.branch=develop
```

# Deploying new airflow

1. login to aws
2. export the configs
```
export AWS_DEFAULT_PROFILE="company-production"
export AWS_DEFAULT_REGION="eu-west-1"
```
3. Login to AWS ECR with
``` 
# for aws cli v1
eval $(aws ecr get-login --no-include-email --region ${AWS_DEFAULT_REGION} | sed 's;https://;;g')  

# for aws cli v2
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
```

4. Build docker image

```
export REGISTRY_URL=123456789.dkr.ecr.eu-west-1.amazonaws.com/ecr_aws_cli
export VERSION_TAG=0.1.0

# Env vars will go into this:
docker build  -f ./Dockerfile . -t ${REGISTRY_URL}:${VERSION_TAG}
docker push ${REGISTRY_URL}:${VERSION_TAG}
```

## Get helm config
(see the #updating-helm-charts at the top for more info)
1. Get the existing chart

```
helm get values airflow -n airflow
```

2. Make any changes (e.g. update database configuration)
3. Save the file to somewhere on your pc, e.g. `/home/user/PROJECTS/values-config/MY-HELM-CHART.yaml`


## Deploy to own namespace
1. Create your namespace
```
kubectl create namespace my-name-prod10 
```
   * Undo later by doing
```
kubectl delete namespace my-name-prod10 
```
2. cd into the folder WITH the helm charts (that has the `charts.yaml` file) and deploy in there.
   * NOTE: the path of the MY-HELM-CHART is **not** the same as the folder with the charts.yaml folder is.

```
cd /home/user/PROJECTS/helm-charts/charts/airflow-deployment

helm upgrade --install airflow . --namespace my-namespace-prod10 --values \
/home/user/PROJECTS/values-config/MY-HELM-CHART.yaml --set environment.branch=develop
```
    
## Running an airflow dag
1. `k9s`
2. Go to the airflow-webserver in your namespace
3. press `shift+f` to portforward to `localhost:8080`
4. Access the airflow UI in your browser at `localhost:8080`


