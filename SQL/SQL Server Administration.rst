SQL SERVER Admin
++++++++++++++++++++

Setting Permissions
======================

1) In Server -> Security -> (Their username or SEC Group)
  a) go to User Mappings
  b) tick the databases they should have access to
  c) Assign db_datareader only (for read only)
  
- `SELECT` permissions only:
   * ✓ db_datareader
   * ✓ public
   
- `SELECT/CREATE/DROP` - Read/Write Permissions:
   * ✓ db_owner
   * ✓ public
