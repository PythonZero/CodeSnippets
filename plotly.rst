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



Plot multiple dfs on a multiple x,y:
=======================================

.. code-block:: python
    
    from plotly.offline import iplot
    iplot(cf.subplots([df1.figure(), 
                 df2.figure(x=['dttm'], y=['Base', 'Peak', 'Off Peak'])
                ], shape=(2, 1)))  
    # it used to be cf.subplots(...).iplot() 
    # now it's iplot(cf.subplots(..))
                

Plot multiple dfs on a single x, y:
========================================

.. code-block:: python


    from plotly.offline import iplot, plot  

    fig1 = df1.iplot(asFigure=True)
    fig2 = df2.iplot(x=['dttm'], y=['Base', 'Peak', 'Off Peak'], asFigure=True)
    # fig1['data'].extend(fig2['data'])  # used to work, but now it's a tuple
    # iplot(fig1) # or plot(fig1) -> saves to file temporarily.
    iplot([*fig1["data"], *fig2["data"]])

Save to html
=========================================

.. code-block:: python


    import cufflinks as cf
    cf.set_config_file(offline=True)
    from plotly.offline import iplot, plot  
    
    fig = df.iplot(asFigure=True)
    plot(fig,filename="df_name.html")
    


Adding text 
=========================================

.. code-block:: python


    fig = df.iplot(asFigure=True)
    fig.update_traces(texttemplate="£%{y:.3s}", textposition="outside") 
    # for formatting options, see https://github.com/d3/d3-format
    # documentation here: https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.html
    fig.update_layout(uniformtext_minsize=10, uniformtext_mode="show")
    
