# Kubernetes commands

## Pods Summary
1. Popeye
 
    ```cmd
    k9s
    # In the pod view press : then search for popeye
    :popeye
    # Return to pod view
    :pod
    ```
2. Get Pod counts
    ```cmd
    kubectl get pods -n your-namespace --no-headers | wc -l
    ```
    
### Listing the reasons for the failed pods:

```cmd
kubectl get all -n <namespace> | head -n 5  # show first 5 rows in cmd
kubectl get all -n default -o custom-columns="RESOURCE:.kind,NAME:.metadata.name,STATUS:.status.phase,X:.status.containerStatuses[].state.waiting.reason"
```

### Deleting the pods which failed

You may want to run this multiple times to make it even faster
```powershell

kubectl get pods -n default -o custom-columns="NAME:.metadata.name,REASON:.status.containerStatuses[].state.waiting.reason" | ForEach-Object {
    $columns = $_ -split '\s+'
    $name = $columns[0]
    $reason = $columns[1]

    if ($reason -eq "ImagePullBackOff") {
        Write-Host "Deleting pod: $name"
        Start-Process -NoNewWindow -FilePath kubectl -ArgumentList "delete", "pod", $name, "-n", "default"
    }
}

```
