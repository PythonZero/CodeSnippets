# Installing statsd

* Statsd is an alternative to prometheus 
* [Old version of statsd (does not support tags)](https://www.bogotobogo.com/DevOps/Docker/Docker_StatsD_Graphite_Grafana.php)
   * ``` 
     docker run -d\
     --name graphite\
     --restart=always\
     -p 80:80\
     -p 81:81\
     -p 2003-2004:2003-2004\
     -p 2023-2024:2023-2024\
     -p 8125:8125/udp\
     -p 8126:8126\
     hopsoft/graphite-statsd   
       ```
       * Might need to change `-p 80:80` -> `-p 800:80` if port 80 is in use (`-p local:container`)
       * Connect graphite to grafana via `localhost:81`  to connect to graphite
       * Has a version of grafana on `localhost:80` or `localhost:800`
       * Default port 8125 to hit statsd endpoint (python / curl ...)

* [New version of statsd (supports tags)](https://hub.docker.com/r/graphiteapp/graphite-statsd/)
  * ```
    docker run -d\
    --name graphite\
    --restart=always\
    -p 80:80\
    -p 2003-2004:2003-2004\
    -p 2023-2024:2023-2024\
    -p 8125:8125/udp\
    -p 8126:8126\
    graphiteapp/graphite-statsd
   ```
     * Might need to change `-p 80:80` -> `-p 800:80` if port 80 is in use (`-p local:container`)
     * Connect to grafana via `localhost:80` or `localhost:800` to connect to graphite
     * has no version of grafana
     * Default port 8125 to hit statsd endpoint (python / curl ...)

## Using Statsd
* Unlike Prometheus, can't go to the `/metrics` endpoint or any url for statsd access 
* Use the Graphite explorer to see the data (or Grafana)

## Python Statsd
```python
import statsd

STATSD_GATEWAY_URL = "localhost"
STATSD_GATEWAY_PORT = 8125 

def inc_counter(type, exception):
    c = statsd.StatsClient(STATSD_GATEWAY_URL, STATSD_GATEWAY_PORT)
    c.incr(f'algo_item_count_total_v2;algo=pe;type={type};exception={exception}')  # tags are semi-colon separated (or comma separated)
    c.incr(f'algo_item_count_total_v2bruh_untagged')  # has no tags

if __name__ == '__main__':
    for _ in range(10):
        inc_counter("start", "bob")
```
