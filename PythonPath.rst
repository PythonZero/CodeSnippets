PYTHON PATH
++++++++++++++++

Allows adding importable locations to python 

Permanently 
***********

Add as Environment Variable:
(check the separator, depends on the OS).

.. code-block:: batch

    PYTHONPATH='C:/path/to/file;.;..;../..;C:/path2/to/another2/file2;'
    # The `.` adds the current directory, ``..`` adds the directory above,


Temporarily
*************

In the command/batch file:

.. code-block:: batch

    SET PYTHONPATH='C:/path/to/file;.;..;../..;'
    python __main__.py
