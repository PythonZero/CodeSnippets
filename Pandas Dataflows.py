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
    
    
if __name__ == "__main__":
    raw_df = pd.DataFrame(...) #i.e. 10 rows x 4 columns
    df = create_empty_df(raw_df)
    populate_df(raw_df, df, 'col1', '', '
