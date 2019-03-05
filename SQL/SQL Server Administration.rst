SQL SERVER Admin
++++++++++++++++++++

Setting Permissions
======================

1) In Server -> Security -> (Their username or SEC Group)

   1) go to User Mappings
   2) tick the databases they should have access to
   3) Assign db_datareader only (for read only)
  
- `SELECT` permissions only (read only):
   * ✓ db_datareader
   * ✓ public
   
- `SELECT/CREATE/DROP` - (Read/Write Permissions):
   * ✓ db_owner
   * ✓ public

Creating db_executor permission
///////////////////////////////
For each database, you must:
   
   
.. code-block:: sql

   -- Create a db_executor role
   CREATE ROLE db_executor

   -- Grant execute rights to the new role
   GRANT EXECUTE TO db_executor
   
Then you can assign :
      * ✓ db_executor
