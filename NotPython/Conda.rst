Conda Commands
+++++++++++++++

Conda environment stuff
=======================


.. code-block:: python

    conda create -n myEnv python=3.5 pip
    activate myEnv
    deactivate
    
    
Creating/Deleting env specific location:

.. code-block:: console

    conda create python=3.7 --prefix = "C:\ProgramData\Anaconda3\envs\testenv"
    activate testenv
    activate
    conda env remove --n testenv



.. code-block:: python
    
    df1 = pd.DataFrame([['2019-01-01', '2019-01-05', 300], 
                        ['2019-01-04', '2019-03-03', 50],
                        ['2019-03-01', '2019-03-05', 500]], 
                  columns=['DttmFrom', 'DttmTo', 'spent'])
    for date_col in ['DttmFrom', 'DttmTo']:
        df1[date_col] = pd.to_datetime(df1[date_col])
