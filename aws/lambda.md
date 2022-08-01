# Lambda

## Creating Layer - Python

1. `pip install --target ./python requests`
   * e.g. to install `requests`
2. Install other packages using that
3. Add any additional code you want to be importable into the `python` folder
   * e.g. `importable_file1.py1` has `def hello_world():print("Hello")`
   * can then `import importable_file1; hello_world()` in your code.
5. Zip the python folder 
   * Make sure the zipped folder starts with a root `python` folder, then with packages inside
6. Example structure
    ```
    python.zip
    |__ python
        |__ importable_file1.py
        |__ importable_package2
        |__ numpy
        |__ pandas
        |__ ...
     ```
   6. Upload zipped file (`python.zip`) to aws (can be named anything)
