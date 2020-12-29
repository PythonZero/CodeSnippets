PyCharm Configuration
======================

Adding anaconda to Pycharm's terminal
--------------------------------------

.. code-block::

    File -> Settings -> Terminal -> Shell path:
    cmd.exe "/k" "D:\Users\<username>\anaconda\Scripts\activate.bat" <Env_Name>


Remote Debugging
---------------------------------------
1) In a separate terminal open a port, e.g. `12345`
    `ssh -R 12345:localhost:12345 user@ip-address`
2) Create a remote debug server with IDE Host Name `localhost` and port `12345`
3) Copy and paste the import statement at the top of the code
.. code-block::python
    import pydevd_pycharm
    pydevd_pycharm.settrace("localhost", port=12345, stdoutToServer=True, stderrToServer=True)
4) Run the debug server in pycharm
5) Run the python code like normal via command line (and put breakpoints in the pycharm version).
    e.g. `python3 <filename.py>` or `spark-submit --pyfiles <filename.py>`
