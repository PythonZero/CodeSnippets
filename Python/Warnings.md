# Warnings


## Simple warnings (See context manager below)

```python
import warnings

def suppressed_warning_function():
     with warnings.catch_warnings():
         # warnings.simplefilter("ignore")  # this alone ignores all warnings.
         warnings.simplefilter(action='ignore', category=RuntimeWarning)  # this filters to only capture RuntimeWarning, other warnings are still raised
         # warnings.simplefilter("error")  # this raises an exception on warning (catch it with `except UserWarning as exc:` or `except Warning as exc:`
         warnings.warn("A custom warning", category=UserWarning)
         warnings.warn("A runtime warning", category=RuntimeWarning)


def test_warning_stuff():
    with pytest.warns(None) as raised_warnings:  # Record warnings
        suppressed_warning_function()

    # Check RuntimeWarnings are suppressed but other warnings are raised
    assert len(raised_warnings.list) == 1
    assert raised_warnings.list[0].category == UserWarning
```

## Context Manager

```python

from contextlib import contextmanager
import warnings

@contextmanager
def ignore_warnings(*warning_types: Type[Warning]):
    """A context manager used to ignore warnings.
    If no warning_types are passed, then all warnings are caught.
    Otherwise, only the specified warning types are caught.

    Usage:

    >>> with ignore_warnings():  # Ignores ALL warnings
    ...    warnings.warn("UserWarning", category=UserWarning)

    >>> with ignore_warnings(UserWarning, ImportWarning):  # ONLY ignores User/ImportWarnings
    ...    warnings.warn("UserWarning", category=UserWarning)

    :param warning_types: The warnings types to ignore
                          (e.g. ImportWarning, DeprecationWarning, ...).
                          Do not pass any arguments to suppress ALL warnings
    """
    with warnings.catch_warnings() as warning_catcher:
        if not warning_types:
            warnings.simplefilter("ignore")  # ignore ALL warnings (if no args passed)

        for warning in warning_types:  # (otherwise) only ignore the specified warnings
            warnings.simplefilter(action="ignore", category=warning)
        yield warning_catcher

```

## Tests

```
import warnings

import numpy as np
import pytest

from pe.algo.utils import ignore_warnings


def test_ignore_warnings__with_arguments():

    with pytest.warns(None) as raised_warnings:  # Record warnings
        warnings.warn("ImportWarning - should NOT be silenced", category=UserWarning)

        with ignore_warnings(RuntimeWarning, UserWarning, ImportWarning):
            warnings.warn("UserWarning - should be silenced ", category=ImportWarning)
            warnings.warn(
                "RuntimeWarning - should be silenced", category=RuntimeWarning
            )
            np.divide(1, 0)  # raises divide by 0 RuntimeWarning - should be silenced
            warnings.warn(
                "DeprecationWarning - should NOT be silenced",
                category=DeprecationWarning,
            )

        warnings.warn("ImportWarning - should NOT be silenced", category=UserWarning)

    # Check RuntimeWarning & Userwarnings are suppressed but other warnings are raised
    assert len(raised_warnings.list) == 3
    assert raised_warnings.list[0].category == UserWarning
    assert raised_warnings.list[1].category == DeprecationWarning


def test_ignore_warnings_no_arguments():

    with pytest.warns(None) as raised_warnings:  # Record warnings
        warnings.warn("ImportWarning - should NOT be silenced", category=ImportWarning)

        with ignore_warnings():
            warnings.warn("UserWarning - should be silenced ", category=UserWarning)
            warnings.warn(
                "RuntimeWarning - should be silenced", category=RuntimeWarning
            )
            np.divide(1, 0)  # raises divide by 0 RuntimeWarning - should be silenced
            warnings.warn(
                "DeprecationWarning - should be silenced", category=DeprecationWarning
            )

        warnings.warn("ImportWarning - should NOT be silenced", category=UserWarning)

    # Check RuntimeWarning & UserWarnings are suppressed but other warnings are raised
    assert len(raised_warnings.list) == 2
    assert raised_warnings.list[0].category == ImportWarning

```
