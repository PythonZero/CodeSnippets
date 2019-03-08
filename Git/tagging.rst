Tagging
=================

Creating a tag
----------------
Tagging the latest commit

.. code-block:: shell

    git tag -a v1.4 -m "my version 1.4"
    git tag -a v1.2 9fceb02  # tag an old version, use the whole checksum (or just a part of it)
    
Pushing the tag to server
---------------------------
  
..code-block:: shell

    git push origin <tagname>
  

Referencing a tagged git (pip)
-------------------------

.. code-block:: shell

    pip install git+https://gitlab.com/myusername/myrepo@v1.2.0
  

Deleting a tag
---------------

.. code-block:: shell

    git tag -d <tagname>.
  
