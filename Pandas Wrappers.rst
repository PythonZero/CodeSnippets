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

Immutable df but with optional single / multiple args
---------------

.. code-block:: python

        def immutable_df(df_arg_name: Union[str, Sequence[str], Callable] = "df"):
            """Converts a function that uses df's to not modify the
            dataframe in place, but rather creates a copy of the df.
            This means that the input df will be unchanged, but
            the output will be provided with an output df.
        
            :param df_arg_name: The names of the argument containing the dataframes.
                                Can take a single name, or multiple names, e.g.
                                "df" or ["df1", "df2", "df3"]
            """
        
            def outer_decorator(func: Callable) -> Callable:
                @functools.wraps(func)
                def inner_decorator(*args, **kwargs):
                    func_signature = inspect.signature(func)
                    func_bound_args = func_signature.bind(*args, **kwargs)
                    func_bound_args.apply_defaults()  # adds the defaults if not passed
        
                    df_arg_names = [df_arg_name] if isinstance(df_arg_name, str) else df_arg_name
                    for df_name in df_arg_names:
                        # Get the dataframe
                        df: pd.DataFrame = func_bound_args.arguments[df_name]
        
                        # Replace it with a copy
                        copied_df = df.copy()
                        func_bound_args.arguments[df_name] = copied_df
        
                    return func(**func_bound_args.arguments)
        
                return inner_decorator
        
            # Handle whether the decorator is passed with or without an argument
            if inspect.isfunction(df_arg_name):
                # no args passed, using the default arg
                function = df_arg_name
                df_arg_name = "df"
                return outer_decorator(function)
        
            # Error message was passed, call the outer decorator
            return outer_decorator

Test:

.. code-block:: python

        def test_immutable_df():
            """Checks if the original dataframe has not been modified"""
        
            @immutable_df  # defaults to df
            def add_3_in_place(df, num, multiplier=3):
                df["added_col"] = num * multiplier
                return df
        
            df_parameters = {"x": [1, 2, 4], "y": ["a", "b", "c"]}
        
            input_df = pd.DataFrame(df_parameters)
            expected_out_df = pd.DataFrame({**df_parameters, "added_col": [3, 3, 3]})
        
            output_df = add_3_in_place(input_df, 1)
        
            # Check that the output dataframe has correctly been modified
            pd.testing.assert_frame_equal(output_df, expected_out_df)
        
            # Check that the input dataframe has not been modified
            pd.testing.assert_frame_equal(input_df, pd.DataFrame(df_parameters))
        
        
        def test_immutable_df_single_non_df_name():
            """Checks if the original dataframe has not been modified"""
        
            @immutable_df("pdf")
            def add_3_in_place(pdf, num, multiplier=3):
                pdf["added_col"] = num * multiplier
                return pdf
        
            df_parameters = {"x": [1, 2, 4], "y": ["a", "b", "c"]}
        
            input_df = pd.DataFrame(df_parameters)
            expected_out_df = pd.DataFrame({**df_parameters, "added_col": [3, 3, 3]})
        
            output_df = add_3_in_place(input_df, 1)
        
            # Check that the output dataframe has correctly been modified
            pd.testing.assert_frame_equal(output_df, expected_out_df)
        
            # Check that the input dataframe has not been modified
            pd.testing.assert_frame_equal(input_df, pd.DataFrame(df_parameters))
        
        
        def test_immutable_df_multiple_non_df_names():
            """Checks if the original dataframe has not been modified"""
        
            @immutable_df(["df1", "df2"])
            def add_3_in_place(df1, df2, num, multiplier=3):
                df1["added_col"] = num * multiplier
                df2["added_col"] = num * multiplier
                return df1, df2
        
            df_parameters = {"x": [1, 2, 4], "y": ["a", "b", "c"]}
        
            input_df1 = pd.DataFrame(df_parameters)
            input_df2 = pd.DataFrame(df_parameters)
            expected_out_df = pd.DataFrame({**df_parameters, "added_col": [3, 3, 3]})
        
            output_df1, output_df2 = add_3_in_place(input_df1, input_df2, 1)
        
            # Check that the output dataframe has correctly been modified
            pd.testing.assert_frame_equal(output_df1, expected_out_df)
            pd.testing.assert_frame_equal(output_df2, expected_out_df)
        
            # Check that the input dataframe has not been modified
            pd.testing.assert_frame_equal(input_df1, pd.DataFrame(df_parameters))
            pd.testing.assert_frame_equal(input_df2, pd.DataFrame(df_parameters))



Df is not empty with optional error message arg
--------------------

.. code-block:: python

        import functools
        from inspect import isfunction
        import pandas as pd
        # from my_file import InputValidation

        def df_output_must_not_be_empty(error_msg: Union[str, Callable] = None) -> Callable:
            """Wrapper that raises a ValidationError if the output dataframe is empty.
            Expects a function with an output of a DataFrame. Takes an optional error message

            >>> @df_output_must_not_be_empty("the dataframe after step 'do_something' is empty")
            ... def do_something(args, kwargs):
            ...     ...
            ...     return df

            >>> @df_output_must_not_be_empty
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

        def test_df_output_must_not_be_empty__errors_because_its_empty():
            @df_output_must_not_be_empty
            def example1_without_msg():
                return pd.DataFrame()

            @df_output_must_not_be_empty("Custom Message")
            def example2_with_msg():
                return pd.DataFrame()

            # TEST that it errors because the dataframes are empty
            with pytest.raises(InputValidation, match="DataFrame is empty when calling"):
                example1_without_msg()

            with pytest.raises(InputValidation, match="Custom Message"):
                example2_with_msg()


        def test_df_output_must_not_be_empty__doesnt_error_if_df_is_not_empty():
            @df_output_must_not_be_empty
            def example3_without_msg_no_error():
                return pd.DataFrame({"x": ["a", "b", "c"]})

            @df_output_must_not_be_empty("Custom Message")
            def example4_with_msg_no_error():
                return pd.DataFrame({"x": ["a", "b", "c"]})

            actual_df = pd.DataFrame({"x": ["a", "b", "c"]})

            # TEST that non-empty df doesn't error AND that the df is correctly returned
            expected_df1 = example3_without_msg_no_error()
            expected_df2 = example4_with_msg_no_error()

            for expected_df in (expected_df2, expected_df1):
                pd.testing.assert_frame_equal(expected_df, actual_df)
