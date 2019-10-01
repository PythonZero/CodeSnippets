Running code in parallel (in jupyter notebook)
++++++++++++++++++++++++++++++++++++++++++++++

- Creates a new thread to run & get the result, giving the thread the queue object.
- Once the result is gotten, the result is put into the queue, ready to be extracted 
  from the main thread.

.. code-block :: python

    import queue
    import threading
    
    def load_sql(sql):
        ...  # loads the query 
        print("Done!")
        return df

    def async_load_sql(sql):   
        """Loads the query. Stores the result into a queue.
           Get the object by doing result.get() """
        def async_load_sql_with_queue(sql, queue):
            queue.put(load_sql(sql))

        q = queue.Queue()        
        t = threading.Thread(target=async_load_sql_with_queue, args=(sql, q))
        t.start()
        return q
    
    
    >>> async_accounts = async_load_sql("""SELECT * FROM accounts """)
    >>> accounts = async_accounts.get()  # run this when "Done!" is printed
