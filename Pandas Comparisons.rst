Array Comparisons
=================

Say you have 2 dataframes of different shapes, you want to broadcast them to be the same shape.
e.g. 

.. code-block:: python
    
    df1 = pd.DataFrame([['2019-01-01', '2019-01-05', 300], 
                        ['2019-01-04', '2019-03-03', 50],
                        ['2019-03-01', '2019-03-05', 500]], 
                  columns=['DttmFrom', 'DttmTo', 'spent'])
    for date_col in ['DttmFrom', 'DttmTo']:
        df1[date_col] = pd.to_datetime(df1[date_col])


    #     DttmFrom     DttmTo    spent
    # 0  2019-01-01  2019-01-05    300
    # 1  2019-01-04  2019-03-03     50
    # 2  2019-03-01  2019-03-05    500
    

And you want to see what you spent for each day:
    
.. code-block:: python

     dates = pd.date_range(start='2019-01-01', end='2019-03-05')
     df2 = pd.DataFrame(columns=dates, index=df1.index)
     df2.loc[0] = dates
     df2.ffill(inplace=True)
     
     
     #   2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     # 0 2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     # 1 2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     # 2 2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     

Then you 
