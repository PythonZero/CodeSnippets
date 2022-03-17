"""Code relating to Monitoring (i.e. Prometheus)"""
from multiprocessing import Manager
from typing import Dict, List

from prometheus_client import Counter


class DelayedCounter:
    _shared_list: List[Dict[str, str]]  # the pending calls
    _manager: Manager

    def __init__(self,  counter: Counter):
        """DelayedCounter should be used when you need a counter in a multiprocess call.
        It records the function that you want to call, and will call it after the
        multiprocessing is complete.
        Instead of passing the counter, pass the DelayedCounter instead.

        Why do we need it?
          * Counter() is not picklable and can't be passed as an argument directly via multiprocessing
          * If you create a separate Counter() within each process, there will be 5 separate counters,
            each with a separate count
            * i.e. if you have 200 items across 5 processes, each Counter will have a count of 40, instead of 200

        How does this solve the problem?
          * It stores each function call into a list

          * Once we exit the context manager, it will call it with the real Counter
            * the main disadvantage is the delay, so the time of the call will be a bit later than the actual time

        Use it as a context manager:

        >>> with DelayedCounter(counter) as delayed_counter:
        ...     # do your thing (i.e. multiprocessing code with Counter calls)
        ... push_to_gateway(PROMETHEUS_GATEWAY, registry=registry, job="algo")

        Example usage:

        >>> import multiprocessing
        >>> from prometheus_client import Counter
        >>> my_counter = Counter("my_counter", "Description", ["label1", "label2", ...], registry=registry)
        >>> def your_function(counter):
        ...     # do some stuff
        ...     counter.labels(x=1, y=2, z=3).inc(2)
        ...
        >>> with DelayedCounter(my_counter) as delayed_counter:
        ...     with multiprocessing.Pool(processes=5) as executor:
        ...         executor.map(your_function, [delayed_counter for _ in range(10)])  # pass the delayed_counter arg
        ...         executor.close()
        ...         executor.join()
        >>> push_to_gateway(PROMETHEUS_GATEWAY, registry=registry, job="algo")


        :param counter: The counter to (eventually) create the calls with - once
                        outside of the context manager / with statement.
        """
        self.counter: Counter = counter

    def __enter__(self):
        """Setup the context manager
        1. Create the shared list (a default python list is not sharable/picklable between processes)
        2. Create the shared list container which does not contain the self.manager (as it is unpicklable)
           and ONLY contains the shared list. It also contains the methods used by Counter."""
        self._setup_shared_list()
        self._shared_list_container = _SharedList(self._shared_list)
        return self._shared_list_container

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager
        1. Makes the (delayed) calls to the real counter
        2. Does the cleanup for the shared list"""
        print(len(self._shared_list))
        self.call()
        self._cleanup_shared_list(exc_type, exc_val, exc_tb)

    def _setup_shared_list(self):
        """Creates a multiprocessing manager list (used to create a sharable list between processes)."""
        self._manager = Manager().__enter__()
        self._shared_list = self._manager.list()
        return self

    def _cleanup_shared_list(self, exc_type, exc_val, exc_tb):
        """Closes and cleans up the multiprocessing manager list and manager itself"""
        self._manager.__exit__(exc_type, exc_val, exc_tb)
        del self._manager
        del self._shared_list

    def call(self):
        """Runs the actual (delayed) calls one at a time, starting from the beginning"""
        for _ in range(len(self._shared_list)):
            # label_kwargs are the counter.labels(...)
            # func_call is the call to be made after the labels e.g. inc for increase
            # func_call_args are the args for the func call, e.g. 1 to
            (label_kwargs, (func_call, *func_call_args)) = self._shared_list.pop(0)

            # the below is the same as: `counter.labels(x=1, y=2, z=3).inc(2)`
            self.counter.labels(**label_kwargs).__getattribute__(func_call)(*func_call_args)


class _SharedList:
    def __init__(self, shared_list):
        """A picklable class that contains the shared list and methods used by Counter

        :param shared_list: a list that can be shared between multiple processes
        """
        self.shared_list = shared_list

    def labels(self, **kwargs):
        return _LabelMethods(self.shared_list).labels(**kwargs)


class _LabelMethods:
    def __init__(self, shared_list):
        """A class to represent the methods available in Counter.labels(...).<METHODS>

        :param shared_list: the shared list containing the arguments to the function calls to the
                            real counter, in the format:
                            [( (kwargs for Counter.labels), (call name after label, the args for the call) )]
        """
        self._shared_list = shared_list
        self._labels_args: Dict

    def labels(self, **kwargs):
        """Store the labels within self, but do nothing with them until a label method is called"""
        self._labels_args = {**kwargs}
        return self

    def inc(self, amount=1):
        """Store the full details of the increment call into the shared list.
        Store into the shared_list the:
           1. the args to the `Counter.labels(*args)`
           2. the 'inc' call to call on Counter.labels
           3. the amount arg for the 'inc' call Counter.labels(*args).inc(amount)"""
        if amount < 0:
            raise ValueError('Counters can only be incremented by non-negative amounts.')
        self._shared_list.append((self._labels_args, ('inc', amount)))

# Below is an example of the simplified version

# class SharedListV2:
#     manager = None
#     the_list = None

#     @classmethod
#     def __enter__(cls):
#         cls.manager = Manager().__enter__()
#         cls.the_list = cls.manager.list()
#         return cls.the_list

#     @classmethod
#     def __exit__(cls, exc_type, exc_val, exc_tb):
#         print("Num items" + "!"*100)
#         print(len(cls.the_list))
#         cls.manager.__exit__(exc_type, exc_val, exc_tb)



###################################################################################
#                                    Tests                                        #
###################################################################################

import multiprocessing
from unittest.mock import MagicMock

from prometheus_client import Counter

from pe.monitoring_utils import DelayedCounter, SharedListV2


def _example_counter_increaser(counter):
    counter.labels(type="test_started", exception=None, country_code="UK").inc()
    counter.labels(type="test_ended", exception="the_exception", country_code="UK").inc()


def test_delayed_counter():
    num_calls = 200
    mocked_registry = MagicMock()
    counter = Counter(
        "my_counter",
        "Count of xxx status per algo",
        ["type", "exception", "country_code"],
        registry=mocked_registry
    )

    with DelayedCounter(counter) as delayed_counter:
        with multiprocessing.Pool(processes=5) as executor:
            executor.map(_example_counter_increaser, [delayed_counter for _ in range(num_calls)])
            executor.close()
            executor.join()

    assert counter._metrics[('test_started', 'None', 'UK')]._value._value == num_calls
    assert counter._metrics[('test_ended', 'the_exception', 'UK')]._value._value == num_calls


# TODO: TEST For the "Easy" version, delete it if you're not using it (only use one or the other)
def _example_counter_increaser_v2(shared_list):
    shared_list.append(dict(something="yes", name="bob"))

def test_delayed_counter_v2():
    num_calls = 200
    with SharedListV2() as shared_list:
        with multiprocessing.Pool(processes=5) as executor:
            executor.map(_example_counter_increaser_v2, [shared_list for _ in range(num_calls)])
            executor.close()
            executor.join()
        assert len(list(shared_list)) == num_calls
        assert list(shared_list) == [{"something": "yes", "name": "bob"}] * 200
