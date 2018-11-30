import pandas as pd



def create_empty_df(raw_df):
    """Create a dataframe of same rows as the raw file"""
    empty_array = np.full((len(raw_df), 1), np.nan)
    df = pd.DataFrame(empty_array)
    return df


def fill_empty_df_dataflow_name(raw_df, empty_df): 
    df = empty_df
    df['colname'] = raw_df[raw_df['col1'] == 'condition']['col8'] # only fills certain rows with the data in col8
    df['GSP'] = raw_df[raw_df['col0'] == 'GSP0']['col4'] 
    # Checks where the row col0 is GSP0, and takes the GSP from column 4.
    df = parse_raw_df(df, raw_df, if_contains='GSP0', in_column='col0', then_extract_from_col='col1', column_name='GSP')
    return df


def parse_raw_df(df: pd.DataFrame, raw_df: pd.DataFrame,  if_contains: str, 
             in_column: str, then_extract_from_col: str, column_name: str):
    """
    Populates the dataframe from the raw_df. 
    :param: raw_df: the dataframe to extract data from
    :param: df: the dataframe with the extracted data - MUST be the same size as raw_df
    :param: if_contains: checks if the raw_df contains this string (raw_df_column_contains)
    :param: in_column: the column to check against (raw_df_column_to_check)
    :param: then_extract_from_col: data to extract from column
    :param: column_name: The column name to call the data
    """
    df[column_name] = raw_df[raw_df[in_column] == if_contains][then_extract_from_col]
    return df
    

def assert_shape_changed(f: Callable[..., pd.DataFrame]) -> Callable[..., pd.DataFrame]:
    """Decorator that checks if the shape of the df before & after are different,
    IFF raise_err = True"""

    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Wrapper that checks if the shape of the dataframe before and after are different
        if raise_arg=True.

        :param args: First argument MUST be df (or df is a kwarg)
        :param kwargs: must contain df as a kwarg if not passed as the first argument.
                       MUST contain 'raise_err' either in the default signature OR
                       kwarg
        :return: output of the function.
        """
        # gets raise_err if passed by the user, else looks up the default kwarg
        raise_err = kwargs.get(
            "raise_err", f.__kwdefaults__["raise_err"]  # type: ignore
        )

        if raise_err:
            df = kwargs["df"] if "df" in kwargs else args[0]
            df_shape = df.shape

        f_out = f(*args, **kwargs)

        if raise_err:
            if df_shape == f_out.shape:
                raise ValueError(
                    "The Shape of the dataframe hasn't changed. "
                    "If you expected the  shape not to change, "
                    f"set {f.__name__}'s argument of"
                    f"'raise_err' to False."
                )

        return f_out

    return wrapper


@assert_shape_changed
def shift_rows(
    df: pd.DataFrame,
    columns_in_that_row: List[str],
    direction: str,
    *,
    raise_err: bool = True,  # pylint: disable=unused-argument
) -> pd.DataFrame:
    """
    :param df: dataframe to shift.
    :param columns_in_that_row: list of columns, e.g. `['Names', 'File Date']
    :param direction: 'up' or 'down'
    :param raise_err: raise an error if the shape hasn't changed.
    :return: df
    Moves all columns (in that row) down into the row below.
                (or shifts up into row above)
    Then that row should be empty, so it will be deleted.
    """
    direction_key = {"up": -1, "down": 1}
    try:
        shift_direction = direction_key[direction.lower()]
    except KeyError:
        raise ValueError("Direction must be either 'up' or 'down' (case-insensitive)")

    df.loc[:, columns_in_that_row] = df.loc[:, columns_in_that_row].shift(
        shift_direction
    )
    df = df.dropna(how="all").reset_index(drop=True)
    return df


def forward_fill_empty_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    :param df: dataframe
    :param cols: list of columns to fill if empty.
                              Uses the previous last non-nan value
    :return: df with columns empty.
    """
    df = df.reset_index(drop=True)

    df.loc[:, cols] = df.loc[:, cols].ffill()
    return df

if __name__ == "__main__":
    raw_df = pd.DataFrame(...) #i.e. 10 rows x 4 columns
    df = create_empty_df(raw_df)
    populate_df(raw_df, df, 'col1', '', '
