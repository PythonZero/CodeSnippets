Python & Coding
================

Main Points
++++++++++++

Variables
------------
- Use full Names - don't abbreviate:
      * Good: ``file_name = 'xyz.csv'``
      * Bad:  ``fn = 'xyz.csv'``
- Use singular verisons of the word when looping on plural
      * Good: ``for file in files:``
      * Bad:  ``for f in files:``

Functions
-----------
- Small and descriptive names
- Should only do 1 thing, and 1 thing well
    * i.e. functions should not have `and`s, e.g. `filter_and_save(df)`
    * What is returned should be logical
- Order of parameters is important
    * The most important variable should be first
- Parameterise the function as much as possible
