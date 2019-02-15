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

1) Broadcast to same shape

.. code-block:: python

     dates = pd.date_range(start='2019-01-01', end='2019-03-05')
     df2 = pd.DataFrame(columns=dates, index=df1.index)
     df2.loc[0] = dates
     df2.ffill(inplace=True)
     
     
     #   2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     # 0 2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     # 1 2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     # 2 2019-01-01 2019-01-02 2019-01-03  ... 2019-03-03 2019-03-04 2019-03-05
     

2) Compare on a cell by cell basis 

.. code-block:: python

    # Doesnt work:   (df2 > df1['DttmFrom']) & (df2 < df1['DttmTo'])
    # so must use: df.gt | .lt | .ge | .le | .ne | .eq 
    df2 = (df2.ge(df1['DttmFrom'], axis=0) & df2.le(df1['DttmTo'], axis=0))

   #     2019-01-01  2019-01-02  2019-01-03  ...  2019-03-03  2019-03-04  2019-03-05
   #  0        True        True        True  ...       False       False       False
   #  1       False       False       False  ...        True       False       False
   #  2       False       False       False  ...        True        True        True
   
   df2 = df2.multiply(df1.spent, axis=0)
   # replaces T/F with that "spent"
   df2.sum()
   
   # 2019-01-01    300
   # 2019-01-02    300
   # 2019-01-03    300
   # 2019-01-04    350
   # 2019-01-05    350
   # 2019-01-06     50
   # ...
   # 2019-02-27     50
   # 2019-02-28     50
   # 2019-03-01    550
   # 2019-03-02    550
   # 2019-03-03    550
   # 2019-03-04    500
   # 2019-03-05    500
