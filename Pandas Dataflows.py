import pandas as pd

raw_df = pd.DataFrame(...) #i.e. 10 rows x 4 columns

def create_empty_df(raw_df):
    """Create a dataframe of same rows as the raw file"""
    empty_array = np.full((len(raw_df), 1), np.nan)
    df = pd.DataFrame(empty_array)
    return df

def fill_empty_df_dataflow_name(raw_df, empty_df)
    df = empty_df
    df['colname'] = raw_df[raw_df['col1'] == 'condition']['col8'] # only fills certain rows with the data in col8
    df['GSP'] = raw_df[raw_df['col0'] == 'GSP']['col4'] 
    # Checks where the row col0 is GSP, and takes the GSP from column 4.
    return df
