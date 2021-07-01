## Deploying a pod within a namespace

1) Create a pod in the existing namespace, e.g. `airflow`

    ```
    kubectl create -f debugging-pod.yaml -n airflow
    ```

2) Create the file `debugging-pod.yaml` (or another name)

    ```
    apiVersion: v1
    kind: Pod
    metadata:
      labels:
        airflow_version: 1.0.0
        kubernetes_pod_operator: "True"
      name: my-pod-name
    spec:
      containers:
      - image: 123456789.dkr.ecr.eu-west-1.amazonaws.com/
      my_ecr_image_name:1.0.0
        imagePullPolicy: Always
        name: base
        command: [ "/bin/bash", "-c", "--" ]
        args: [ "while true; do sleep 30; done;" ]
        env:
        - name: MY_USER_EXECUTION_ROLE_ARN
          value: arn:aws:iam:123456789:role/my-operator-role
        - name: AWS_DEFAULT_REGION
          value: eu-west-1
    ```

3) In `k9s`, attach to your shell using `s` NOT `a`

## k9s commands

* Only view your namespace:
    - press `shift + ;`
    - type `namespace` (it will then list all the available namespaces)
    - select your namespace (e.g. `airflow`)
    - press enter
    - you should now only see pods within your namespace
