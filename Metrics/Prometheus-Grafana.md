# Prometheus Set up

1) Download & Install the prometheus server from https://prometheus.io/download/
   * This provides you with the dashboard to access prometheus
   * It will run on `localhost:9090`

# Grafana Set up
1) Install Grafana (Enterprise edition is ok)
2) Access it on `localhost:3000`
3) Click the cog on the left
4) Click on Data sources
5) Add data source
6) Prometheus
7) Use the Url `localhost:9090`
8) You are now able to access Prometheus in Grafana

## Machine metrics (Windows / Node explorer) on Prometheus
1) Download & run node_explorer 
    * Windows_explorer for windows https://github.com/prometheus-community/windows_exporter/releases 
    * This provides metrics from your machine to prometheus
2) Connect the node_explorer / windows_explorer to the prometheus server by editing the `prometheus.yml` file 
    *   ```yaml
        scrape_configs:
        - job_name: "prometheus"
          static_configs:
            - targets: ["localhost:9090"]
        - job_name: "windows_scrape"
          static_configs:
            - targets: ["localhost:9182"]
        ```
3) Restart the grafana server
4) You should now be able to access the metrics from `localhost:9090`
   * Create a dashboard using one of the metrics, e.g. `windows_cs_physical_memory_bytes`

## Python metrics on Prometheus

1) Create a basic python file with a metric, e.g. `request_processing_seconds` and `my_failures` 
    * ```python
      from prometheus_client import start_http_server, Summary, Counter
      import random
      import time

      # Create a metric to track time spent and requests made.
      REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

      # Decorate function with metric.
      @REQUEST_TIME.time()
      def process_request(t):
          """A dummy function that takes some time."""
          time.sleep(t)


      if __name__ == '__main__':
          # Start up the server to expose the metrics.
          start_http_server(8000)

          c = Counter('my_failures', 'Description of counter')
          c.inc()  # Increment by 1
          c.inc(1.6)  # Increment by given value

          # Generate some requests.
          n = 0
          while True:
              print(f"Request {n}")
              n += 1
              process_request(random.random())

      ```
 
2) Update the `prometheus.yml` to also scrape from the new server (8000)
    *   ```yaml
        scrape_configs:
        - job_name: "prometheus"
          static_configs:
            - targets: ["localhost:9090", "localhost:8000"]
         ```

3) Restart the grafana server
4) You should now be able to select the two new metrics (`my_failures<_created>`, `request_processing_seconds<_sum>`)
