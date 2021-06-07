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

Df is not empty with optional error message arg
--------------------

.. code-block:: python

        import functools
        from inspect import isfunction
        import pandas as pd
        # from my_file import InputValidation

        def validate_df_is_not_empty(error_msg: Union[str, Callable] = None) -> Callable:
            """Wrapper that raises a ValidationError if the output dataframe is empty.
            Expects a function with an output of a DataFrame. Takes an optional error message

            >>> @validate_df_is_not_empty("the dataframe after step 'do_something' is empty")
            ... def do_something(args, kwargs):
            ...     ...
            ...     return df

            >>> @validate_df_is_not_empty
            ... def process_dataframe(args, df):
            ...     return df

            :param error_msg: Optional error message to be output with the ValidationError
            :return: Wrapper that checks if the output dataframe is not empty
            """

            def outer_decorator(func: Callable):
                @functools.wraps(func)
                def inner_decorator(*args, **kwargs) -> pd.DataFrame:
                    df = func(*args, **kwargs)
                    if df.empty:
                        raise InputValidation(errors=[error_msg])
                    return df

                return inner_decorator

            # Handle whether the decorator is passed with or without an argument

            if isfunction(error_msg):
                # no error message passed, using the default error message
                function = error_msg
                error_msg = f"DataFrame is empty when calling {function.__name__}"
                return outer_decorator(function)

            # Error message was passed, call the outer decorator
            return outer_decorator
            
Test:

.. code-block:: python

        def test_validate_df_is_not_empty__errors_because_its_empty():
            @validate_df_is_not_empty
            def example1_without_msg():
                return pd.DataFrame()

            @validate_df_is_not_empty("Custom Message")
            def example2_with_msg():
                return pd.DataFrame()

            # TEST that it errors because the dataframes are empty
            with pytest.raises(InputValidation, match="DataFrame is empty when calling"):
                example1_without_msg()

            with pytest.raises(InputValidation, match="Custom Message"):
                example2_with_msg()


        def test_validate_df_is_not_empty__doesnt_error_if_df_is_not_empty():
            @validate_df_is_not_empty
            def example3_without_msg_no_error():
                return pd.DataFrame({"x": ["a", "b", "c"]})

            @validate_df_is_not_empty("Custom Message")
            def example4_with_msg_no_error():
                return pd.DataFrame({"x": ["a", "b", "c"]})

            actual_df = pd.DataFrame({"x": ["a", "b", "c"]})

            # TEST that non-empty df doesn't error AND that the df is correctly returned
            expected_df1 = example3_without_msg_no_error()
            expected_df2 = example4_with_msg_no_error()

            for expected_df in (expected_df2, expected_df1):
                pd.testing.assert_frame_equal(expected_df, actual_df)
