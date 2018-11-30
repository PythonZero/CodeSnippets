# Plot.ly quick commands:

##Add dash .iplot() to a dataframe
    
    import cufflinks as cf
    cf.set_config_file(offline=True, world_readable=False )
    df.iplot()


## Plot multiple subplots single plot:

    cf.subplots([df1.figure(), 
                 df2.figure(x=['dttm'], y=['Base', 'Peak', 'Off Peak'])
                ], shape=(2, 1)).iplot()
