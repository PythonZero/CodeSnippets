# Prometheus / Grafana

## Set up
1. Install Prometheus client
    * http://localhost:9090
2. Install Prometheus Gateway
    * http://localhost:9091
3. Install Grafana (optional)
    * http://localhost:3000

* Setup prometheus.yml to connect to the pushgateway
    ```yaml
    scrape_configs:
      - job_name: pushgateway
        honor_labels: false
        static_configs:
            - targets: ['localhost:9091']
     ```
* Run all 3 via cli (open in cmd)
    - check http://localhost:9090/config & http://localhost:9090/targets
      to ensure pushgateway is connected

* Can either push to Gateway via curl / python library
  * Access data pushed via http://localhost:9091/metrics

* Query the data in grafana
  * http://localhost:9090/graph 
  * Example queries:
    1. `sum(custom_item_count_v2_total{type="started"})`
      * Gets the sum (the count) at each time point 
      * filters by `{type="started"}`
    2. `sum_over_time(custom_item_count_v2_total[15s])`
      * Gets the sum over that time period - if you do it this way,
        it is good to use the scrape timer (i.e. `15s`).
           * That way all metrics that are scraped in that time frame count 
             towards the same data point
           * Otherwise if you do `30s`, it will also sum again the
             previous scrape (which could lead to duplicates)
    3. `sum(sum_over_time(custom_item_count_v2_total{type="completed"}[15s])
            or
            sum_over_time(custom_item_count_v2_total{type="fail"}[15s]))`

## Tips

* Registry should be top level
* Once you create a `Counter(..., registry)`, you should add labels and increment it.
  * do NOT create a new counter, otherwise it will restart to 1 (when you push the metrics to gateway)


## Troubleshooting
* If you get HTTP Bad request, it may be because you're trying to push too
  many metrics (which are backlogged)
* Or maybe you are trying to push corrupted data
  * I Deleted the files in the PROMETHEUS_MULTIPROC_DIR and it fixed the error
  * But the error was happening because the messages weren't correctly formatted 
    when using multiprocessing (it corrupted the output)
