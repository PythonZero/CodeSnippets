Array Comparisons
=================

The wrapper:

.. code-block:: python
    
    """Wrappers for functions"""

    import functools
    import inspect
    from collections import Callable

    import pandas as pd


    def immutable_df(func: Callable) -> Callable:
        """Converts a function that uses df's to not modify the
        dataframe in place, but rather creates a copy of the df.
        This means that the input df will be unchanged, but
        the output will be provided with an output df.
        MUST take the argument (or kwarg) "df".
        """

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            func_signature = inspect.signature(func)
            func_bound_args = func_signature.bind(*args, **kwargs)
            func_bound_args.apply_defaults()  # adds the defaults if not passed

            # Get the dataframe
            df: pd.DataFrame = func_bound_args.arguments['df']

            # Replace it with a copy
            copied_df = df.copy()
            func_bound_args.arguments['df'] = copied_df

            return func(**func_bound_args.arguments)

        return wrapped_func


Test:

.. code-block:: python

    import pandas as pd

    from .wrappers import immutable_df


    def test_immutable_df():
        """Checks if the original dataframe has not been modified"""

        @immutable_df
        def add_3_in_place(df, num, multiplier=3):
            df['added_col'] = num*multiplier
            return df

        df_parameters= {"x": [1, 2, 4], "y": ["a", "b", "c"]}

        input_df = pd.DataFrame(df_parameters)
        expected_out_df = pd.DataFrame(
            {**df_parameters, "added_col": [3, 3, 3]}
        )

        output_df = add_3_in_place(input_df, 1)

        # Check that the output dataframe has correctly been modified
        pd.testing.assert_frame_equal(output_df, expected_out_df)

        # Check that the input dataframe has not been modified
        pd.testing.assert_frame_equal(input_df, pd.DataFrame(df_parameters))

