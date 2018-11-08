# How to use Sphinx - Auto Documentation

1) `cd` into your python project path
2) `sphinx-quickstart docs` (where `docs` is the folder location sphinx will be created in`
     - use all the default settings, except for the modules, use `autodoc` and whichever ones you want
3) In `docs\conf.py` 
    - Scroll to the path setup
    - Uncomment the `sys.path` stuff, and replace it with:
        - `sys.path.insert(0, (os.path.join(__file__, '../')))`  
        - (this is the location where autodocs looks for the python code).
4) Can create the skeleton (check if everything worked correctly) by `docs\make.bat html` 
5) Can then delete it by `docs\make.bat clean` - removes everything in the _build
6) Autogenerate the sphynx code from your codebase:
    - `sphinx-apidoc -f -o "docs\rst" .`
        - `sphinx-apidoc` = the code generatr
        - `-f` = force (overwrites existing files)
        - `-o "docs\rst"` = output location (creates an rst folder containing all the reStructuredText files of our code)
        - `.` = the location of our code
7) `docs\make.bat clean`
8) `docs\make.bat html`

In `conf.py`:
add at the bottom of the code `add_module_names = False` - gets rid of `project_name.module.submodule.functionname` with `functionname`
