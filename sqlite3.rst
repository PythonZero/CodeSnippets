Locate where the sqlite database is
------------------------------------

  .. code-block:: python 

  conn.execute("PRAGMA database_list").fetchall()[0] # or [1], [2], ...
