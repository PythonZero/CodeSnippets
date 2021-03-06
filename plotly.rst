Plot.ly quick commands:
-------------------------

Add plotly .iplot() to a dataframe
==================================

.. code-block:: python    

    import cufflinks as cf
    cf.set_config_file(offline=True, world_readable=False )
    df.iplot()


Modify config of iplot
========================

.. code-block:: python

    fig = df.iplot(asFigure=True)
    # change the setting, i.e. hovermode
    fig.layout["hovermode"] = "x"
    plotly.offline.iplot(fig)



Plot multiple subplots on a single plot:
=======================================

.. code-block:: python

    cf.subplots([df1.figure(), 
                 df2.figure(x=['dttm'], y=['Base', 'Peak', 'Off Peak'])
                ], shape=(2, 1)).iplot()

Plot multiple dfs on a single x, y:
========================================

.. code-block:: python


    from plotly.offline import iplot, plot  

    fig1 = df1.iplot(asFigure=True)
    fig2 = df2.iplot(x=['dttm'], y=['Base', 'Peak', 'Off Peak'], asFigure=True)
    fig1['data'].extend(fig2['data'])
    iplot(fig1) # or plot(fig1) -> saves to file temporarily.

Save to html
=========================================

.. code-block:: python


    import cufflinks as cf
    cf.set_config_file(offline=True)
    from plotly.offline import iplot, plot  
    
    fig = df.iplot(asFigure=True)
    plot(fig,filename="df_name.html")
