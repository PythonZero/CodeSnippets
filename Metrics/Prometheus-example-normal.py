import random
import time

from prometheus_client import CollectorRegistry, Counter, push_to_gateway


PROMETHEUS_PUSH_GATEWAY = "localhost:9091"


def _push_metrics(registry):
    push_to_gateway(PROMETHEUS_PUSH_GATEWAY, registry=registry, job="pe")


def setup():
    registry = CollectorRegistry()
    counter = Counter(
        "custom_item_count_v2",
        "The description for custom item count v2",
        ["type", "exception", "item_id"],
        registry=registry,
    )
    return registry, counter


def example_counter(registry, counter):
    counter.labels(type="started", exception="None", item_id=1234).inc()
    _push_metrics(registry)

    counter.labels(type="completed", exception="None", item_id=1234).inc()

    if random.random() > 0.4:
        counter_exception = random.choice(["ValueError", "YeahhBuddyError", "TypeError"])
        counter.labels(type="failure", exception=counter_exception, item_id=1234).inc()

    _push_metrics(registry)


if __name__ == '__main__':
    registry, counter = setup()
    for i in range(80):
        example_counter(registry, counter)
        time.sleep(0.5)
        print(i)


# Example output after the run
"""
# HELP custom_item_count_v2_created The description for custom item count v2
# TYPE custom_item_count_v2_created gauge
custom_item_count_v2_created{exception="TypeError",instance="",job="pe",type="failure"} 1.6473095961612914e+09
custom_item_count_v2_created{exception="ValueError",instance="",job="pe",type="failure"} 1.6473096009401855e+09
custom_item_count_v2_created{exception="YeahhBuddyError",instance="",job="pe",type="failure"} 1.647309600433455e+09
custom_item_count_v2_created{exception="none",instance="",job="pe",type="completed"} 1.6473095961612914e+09
custom_item_count_v2_created{exception="none",instance="",job="pe",type="started"} 1.6473095961299686e+09
# HELP custom_item_count_v2_total The description for custom item count v2
# TYPE custom_item_count_v2_total counter
custom_item_count_v2_total{exception="TypeError",instance="",job="pe",type="failure"} 22
custom_item_count_v2_total{exception="ValueError",instance="",job="pe",type="failure"} 25
custom_item_count_v2_total{exception="YeahhBuddyError",instance="",job="pe",type="failure"} 22
custom_item_count_v2_total{exception="none",instance="",job="pe",type="completed"} 100
custom_item_count_v2_total{exception="none",instance="",job="pe",type="started"} 100
# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles.
# TYPE go_gc_duration_seconds summary
... [the default prometheus metrics]
"""
# total of 69 errors
# 100 started & 100 completed
