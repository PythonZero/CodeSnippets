# Plot.ly quick commands:
-------------------------

## Add plotly .iplot() to a dataframe
    
    import cufflinks as cf
    cf.set_config_file(offline=True, world_readable=False )
    df.iplot()


## Plot multiple subplots on a single plot:

    cf.subplots([df1.figure(), 
                 df2.figure(x=['dttm'], y=['Base', 'Peak', 'Off Peak'])
                ], shape=(2, 1)).iplot()

## Plot multiple dfs on a single x, y:

    from plotly.offline import iplot, plot  

    fig1 = df1.iplot(asFigure=True)
    fig2 = df2.iplot(x=['dttm'], y=['Base', 'Peak', 'Off Peak'], asFigure=True)
    fig1['data'].extend(fig2['data'])
    iplot(fig1) # or plot(fig1) -> saves to file temporarily.

## Save to html
    import cufflinks as cf
    cf.set_config_file(offline=True)
    from plotly.offline import iplot, plot  
    
    fig = df.iplot(asFigure=True)
    plot(fig,filename="df_name.html")
