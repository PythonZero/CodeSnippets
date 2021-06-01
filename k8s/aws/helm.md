# Updating helm charts

1. Get existing helm chart 

```
helm get values airflow -n airflow
```

2. Save these values somewhere (e.g. /home/user/PROJECTS/values-config/my-chart.yaml )

3. Make any changes to the charts (e.g. update the sql database)

4. SUPER IMPORTANT - change directory INTO the folder with the Charts.yaml file, e.g.

```
cd /home/user/PROJECTS/helm-charts/airflow/deployment
```

5. Deploy the updated helm charts 
```
helm upgrade --install airflow . --namespace my-namespace-prod1 --values /home/user/PROJECTS/values-config/my-chart.yaml  --set environment.branch=develop
```
