Pytest
----------------

MonkeyPatching
================

.. code-block:: python
    
    ## PythonPath to A:   BasePath.Module.SubModule.A
    # File A:
    def bar(): return 5

    # File B:
    def add_two_numbers(x):
      return x + bar()

    # Test File
    def test_add_two_numbers(monkeypatch):
      def new_bar(): print('patched'); return 10
      print(add_two_numbers(3)) # Output = 8
      monkeypatch.setattr('BasePath.Module.SubModule.B.bar',  # < -- IMPORTANT, you load it from B.py not A.py!!!!!!!
      new_bar)
      print(add_two_numbers(3)) # Prints 'Patched' & Outputs = 13


Adding argument(s) to Fixture
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
