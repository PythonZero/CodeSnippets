Pytest
----------------

MonkeyPatching
================

Another Way to Patch (with conftest pattern)
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python
    
   import file1
   # conftest.py
   def mock_item_getter(monkeypatch):
       def mock_some_specific_function_in_item_getter(arg1, arg2):
           return arg1 + arg2
       # note how file1 is not a string,the other examples use strings
       monkeypatch.setattr(file1, "some_specific_function_in_item_getter", mock_some_specific_function_in_item_getter)
   
   # test_utils.py
   def test_something(mock_item_getter):
       # write your test as normal
       pass

Functions in different Files
+++++++++++++++++++++++++++++
.. code-block:: python
    
    ## PythonPath to A:   BasePath.Module.SubModule.A
    # File A:
    def bar(): 
        return 5

    # File B:
    def add_two_numbers(x):
      return x + bar()

    # Test File
    def test_add_two_numbers(monkeypatch):
      def new_bar(): print('patched'); return 10
      print(add_two_numbers(3)) # Output = 8
      monkeypatch.setattr('BasePath.Module.SubModule.B.bar', new_bar) # < -- IMPORTANT, you load it from B.py not A.py!!!!!!!
      print(add_two_numbers(3)) # Prints 'Patched' & Outputs = 13


Functions in same File
++++++++++++++++++++++

.. code-block:: python
    
    # File A:
    def bar(): 
        return 5
    def add_two_numbers(x):
      return x + bar()
    
    # test file
    import file_a  # <-- NOT `from file_a import add_two_numbers`. **MUST** import it this way 
    
    
    def test_add_two_numbers(monkeypatch):
      def new_bar(): print('patched'); return 10
      monkeypatch.setattr('filea.bar', new_bar) # < -- IMPORTANT, must do `filea.xx`
      print(file_a.add_two_numbers(3)) # Prints 'Patched' & Outputs = 13

See stackoverflow_ for more details

.. _stackoverflow: https://stackoverflow.com/questions/31306080/pytest-monkeypatch-isnt-working-on-imported-function

     
Patching a default argument
+++++++++++++++++++++++++++++++
If you want to patch for example `x = 10` into `x = 100`, you can't patch `x`, must patch the function

.. code-block:: python

   # file 1
   x = 10
   def foo(a, b=x, c=2):   
      return a + b + c)
   
   # file 2
   from file1 import foo
   def crazy(a):
       foo(a)
       
   # test file
   def test_foo():
       def patched_foo(a): return foo(a, b=100, c=2)
       monkeypatch.setattr('file2.foo', patched_foo)
       
   

Patching Environment Variables
=================================

.. code-block:: python
    
    def test_conn(monkeypatch):
        monkeypatch.setenv('DATABASE_URL', 'Patched_URL')
        monkeypatch.delenv(name, raising=True)
        # Do stuff with patched environment

Note:

.. code-block:: python
        
        monkeypatch.setenv(name, value, prepend=None) # prepend saves the existing env variable
        # e.g. name = monkeypatch.setenv('DATABASE_URL', 'google.com', prepend = '_'),
        # Then there will be {'DATABASE_URL': 'google.com' , '_DATABASE_URL': 'old_value'} 

Adding argument(s) to Fixture & Temporary path
==========================
.. code-block:: python

    @pytest.fixture
    def create_temporary_file(request, tmpdir):     # request MUST be a parameter, tmpdir is a fixture with the tmpdir location
        filename = request.param                    # the request object's param contains the values passed to it by the decorator
        path = tmpdir / filename
        yield path
    
    # pass multiple args by [['bob', 'k', 3]] & access by name, ... = request.param[0], [1], [2]:
    @pytest.mark.parametrize('create_temporary_file', ['config.yaml'], indirect=True)   # indirect = True,  important!
    def test_load_file(create_temporary_file):
        path = create_temporary_file
        path.write('this is what will be in the text file..!')
        

Adding arguments to Fixture AND test 
==========================
.. code-block:: python

    def person_says(name, age):
    return f"{name} is {age}"


    @pytest.fixture
    def add_surname(request):
        surname = request.param
        return f'Mike {surname}'


    NAME1 = "Johnson"
    AGE1 = "13"
    OUTPUT1 = "Mike Johnson is 13"
    NAME2 = "Liam"
    AGE2 = "21"
    OUTPUT2 = "Mike Liam is 21"


    @pytest.mark.parametrize('add_surname,age,expected', 
                             [[NAME1, AGE1, OUTPUT1], [NAME2, AGE2, OUTPUT2]],
                             indirect=['add_surname'])
    def test_person_says(add_surname, age, expected):
        name = add_surname
        output = person_says(name, age)
        assert expected == output

Some Notes:
1) if you had a fixture function that took 0 arguments,  you MUST still give it a parameterized argument, e.g.

.. code-block:: python


    @pytest.fixture
    def clean_database():
        print("Cleaned")

    @pytest.mark.parametrize("clean_database,greeting", [(None, "hello")], indirect=["clean_database"])
        def test_greet(clean_database, greeting):
            print(greeting)


2) setting `indirect = False`, means all the arguments are local parameters
   setting `indirect = True`, means all the arguments are fixture parameters
   setting `indirect = ['function_name']`, means only to use that argument as a fixture parameter
        
CapSys or capfd (Capture the print)
==================================

.. code-block:: python
        
    def test_print_10(capsys):
        print("10")
        out, err = capsys.readouterr()
        assert '10' in out


    def test_print_10(capfd): # or replace capsys w/capfd - capfd also captures libraries & subprocesses
        print("10")
        sys.stderr.write("20")
        out, err = capfd.readouterr()  # readouterr captures all prints till now. (then resets it)
        assert '10\n' == out # prints go to out
        assert '20' == err # sys.stderr goes to err
        print("30")
        out, err = capfd.readouterr()
        assert '30\n' == out


CapLog (Capture the Log)
==============================

.. code-block:: python

    def test_capture_log(caplog):
        caplog.set_level(logging.DEBUG)
        # ...
        assert 'abcd' in caplog.text
        # caplog.text, caplog.records, caplog.record_tuples, caplog.clear()

Error Message Checking
================

.. code-block:: python
    
    def test_something():
        
        # match takes regex
        with pytest.raises(KeyError, match='hahaha .* for') as e:
            raise KeyError('hahaha you stupidddddddd so whats for dinner')
        
        assert 'stupiddddd' in str(e.value)
    
    
Testing Tree
===================

.. code-block::
        
    tests
    |________ integration
    |         |___test_i_module1    # can't use the same name as unit/test_module1, so add an `_i_`
    |
    |________ unit
                |__test_module1
                |__test_module2


Make fixtures appear across all modules
========================================

Put fixtures in a conftest.py

.. code-block:: python

    # conftest.py
    @pytest.fixture(scope="session", autouse=True)
    def gcp_setup():
        print("SETTING UP GCP BUCKETS AND DATASET")
        yield
        print("TEARING DOWN GCP BUCKETS AND DATASET")
    
    @pytest.fixture
    def hello():
        print("Hello")
    

If autouse=True, then it will run regardless.
You can then use those fixtures without needing to import them, e.g.


.. code-block:: python

    # test_file.py
    def test_function(hello):
        assert 5+5 == 10
    
    # Output
    # SETTING UP GCP BUCKETS AND DATASET
    # Hello
    # TEARING DOWN GCP BUCKETS AND DATASET
   
   

Mocking
=================================

.. code-block:: python
    
    from mock import Mock, MagicMock  # 1 of the 2, but prefer MagicMock over Mock as it has special methods
    
    # Mocking class properties
    mocked_args = mock.Mock(arg1=3000)
    mocked_args.a = 1
    mocked_args.b = [1, 2, 3]
    print(mocked_args.a) # 1
    print(len(mocked_args.b)) # [1,2,3]
    
    # Mocking class methods
    mocked_args.my_func.return_value = ["file1", "file2"]
    assert mocked_args.my_func("any", "number", "of", "arguments", 123) == ["file1", "file2"]
    
    
    # MagicMock vs Mock, has some methods built in, e.g.
    len(mock.MagicMock(x=1, y=2))  # returns 0
    len(mock.Mock(x=1, y=2))  # errors


Mocking Datetime
++++++++++++++++++++

.. code-block:: python

    class MockedDatetime:
        @classmethod
        def now(cls, *args, **kwargs):
            return datetime(2021, 5, 2)

    # change datetime.now()'s date
    monkeypatch.setattr("root.folder.file1.datetime", MockedDatetime)

    


Ignoring doctests
==================================

```
>>> some_code('x', 'y', 'z') # doctest: +SKIP
```
