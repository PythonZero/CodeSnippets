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
        
    @pytest.mark.parametrize('create_temporary_file', ['config.yaml'], indirect=True)   # INDIRECT = TRUE! important
                        # pass multiple args by [['bob', 'k', 3]] & access by name, ... = request.param[0], [1], [2]
    def test_load_file(create_temporary_file):
        path = create_temporary_file
        path.write('this is what will be in the text file..!')
        

        
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
