# Problem with this method is that the counter is re-created on each instance
#   and only (200 runs / 5 proccesses) = 40 runs are recorded & the other 60 are lost.
# See the delayed counter solution


import random
import multiprocessing

from prometheus_client import CollectorRegistry, Counter, push_to_gateway, multiprocess

PROMETHEUS_PUSH_GATEWAY = "localhost:9091"


def _push_metrics(registry):
    push_to_gateway(PROMETHEUS_PUSH_GATEWAY, registry=registry, job="pe")


def setup():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry, path=r"C:\Users\bob\prometheus")
    counter = Counter(
        "custom_item_count_v2",
        "The description for custom item count v2",
        ["type", "exception"],
        registry=registry,
    )
    return registry, counter


def example_counter(_):
    counter.labels(type="started", exception="none").inc()
    _push_metrics(registry)

    counter_exception = (
        "none" if random.random() < 0.4 else random.choice(["ValueError", "YeahhBuddyError", "TypeError"])
    )
    counter.labels(type="completed", exception=counter_exception).inc()
    counter.labels(type="failure", exception=counter_exception).inc()
    _push_metrics(registry)



registry, counter = setup()
if __name__ == "__main__":
    with multiprocessing.Pool(processes=5) as executor:
        outputs = executor.map(example_counter, [_ for _ in range(200)])
        executor.close()
        executor.join()
# Problem with this method is that the counter is re-created on each instance
#   and only (200 runs / 5 proccesses) = 40 runs are recorded & the other 60 are lost.
# See the delayed counter solution
