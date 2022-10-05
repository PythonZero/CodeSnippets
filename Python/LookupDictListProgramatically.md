# Lookup
## Problem:
   * Say you had a complicated dictionary (or list), and wanted to find a value that is nested deep, e.g.
     * `my_dict = {"x": {"a": [1, 2, 3],"b": [2, 1, 3],"c": [1, 4, 5], "d": {"e": {"f": [{"gasdasd": 0}]}},}}`
   * You want to repeatedly getting / setting `my_dict["x"]["d"]["e"]["f"]`
   * You don't want to keep typing the full slice
## Solution
```python
from typing import Container, Callable, Dict, Union, Tuple

my_dict = {
    "x": {
        "a": [1, 2, 3],
        "b": [2, 1, 3],
        "c": [1, 4, 5],
        "d": {"e": {"f": [{"gasdasd": 0}]}},
    }
}

my_dict_lookup_rules = {
    "rule1": (lambda container: container["x"]["d"]["e"], "f"),
    "rule2": (lambda container: container["x"]["a"], 0),
    "rule3": (lambda container: container, "a"),
}

def lookup(
    container: Container,
    lookup_rule: str,
    set_=False,
    value=None,
    lookup_rules: Dict[str, Tuple[Callable, Union[str, int]]] = my_dict_lookup_rules,
):
    """

    :param container: The container (e.g. a dict / list / set )
    :param lookup_rule: The rule name for that dict
    :param lookup_rules: The rules list
        FORMAT of the lookup rules:
        e.g. to access x[1][2]["a"][3], the rule should be
        { "rule1": (lambda x: x[1][2]["a"], 3)}
        * NOTE: the last value must be separated as a 2nd item in the tuple
    :param set_: If false, only gets the item.
                *WARNING* If True, sets the item (replaces or adds).
    :param value: The value that will be set. This is only used if set=True
    :return: The value get/set
    """
    if lookup_rule not in lookup_rules:
        raise NotImplementedError(
            f"The rule '{lookup_rule}' has not been created for the dict. "
            f"Choose from '" + "','".join(lookup_rules.keys()) + "'"
        )
    container_getter, last_index = lookup_rules.get(lookup_rule)

    if set_:
        container_getter(container).__setitem__(last_index, value)

    return container_getter(container)[last_index]


```

Tests
```python

my_dict = {
    "x": {
        "a": [1, 2, 3],
        "b": [2, 1, 3],
        "c": [1, 4, 5],
        "d": {"e": {"f": [{"gasdasd": 0}]}},
    }
}

super_complicated_dict = {"a": {"b": {"c": {"d": [13, {"e": [{"f": "g"}]}]}}}}

my_dict_lookup_rules = {
    "rule1": (lambda container: container["x"]["d"]["e"], "f"),
    "rule2": (lambda container: container["x"]["a"], 0),
    "rule3": (lambda container: container, "a"),
}

super_complicated_dict_lookup_rules = {
    "get_the_last_thing": (
        lambda container: container["a"]["b"]["c"]["d"][1]["e"][0],
        "f",
    )
}

def test_lookup_get():
    # Get from a dict
    x1 = lookup(my_dict, "rule1")
    # Get from a list
    x2 = lookup(my_dict, "rule2")
    # Get from a separate lookup_rules
    x3 = lookup(
        super_complicated_dict,
        "get_the_last_thing",
        lookup_rules=super_complicated_dict_lookup_rules,
    )
    assert x1 == [{"gasdasd": 0}]
    assert x2 == 1
    assert x3 == "g"


def test_lookup_set():
    # set a dict
    get_value = lookup(my_dict, "rule1")
    assert get_value != 13  # check it's not changed
    set_value = lookup(my_dict, "rule1", set_=True, value=13)
    assert set_value == 13

    # set a list
    get_value2 = lookup(my_dict, "rule2")
    assert get_value2 != 14  # check it's not changed
    set_value2 = lookup(my_dict, "rule2", set_=True, value=14)
    assert set_value2 == 14

```
