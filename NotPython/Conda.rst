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
