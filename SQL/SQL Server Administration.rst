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
   GRANT EXECUTE, VIEW DEFINITION TO db_executor
   -- DON'T GIVE ALTER ACCESS:
   -- GRANT ALTER, EXECUTE, VIEW DEFINITION to db_executor 
   
Then you can assign :
      * ✓ db_executor


Setting Permissions Using T-SQL
================================
1) When ticking the database box in User Mappings (step 2) in `Setting Permissions`),
   it creates a user in that database
  
   * User is mapped to that database
   
2) When ticking the box in the "Database role membership for: <db_name>"
   it assigns the role to the user
  
.. code-block:: sql

   CREATE USER [<username>] FROM LOGIN [<username>]  -- step 1 
   ALTER ROLE [<role_name>] ADD MEMBER [<username>]  -- step 2
   
Example:

.. code-block:: sql
 
   CREATE USER [DOMAIN\bob] FROM LOGIN [DOMAIN\bob] 
   ALTER ROLE [db_executor] ADD MEMBER [DOMAIN\bob] 

 
