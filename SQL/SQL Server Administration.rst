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
