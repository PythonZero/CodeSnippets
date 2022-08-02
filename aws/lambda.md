# Lambda

## Creating Layer - Python

**Troubleshooting** 
  - Not running these instructions on a unix-like OS may cause errors 
  - Make sure you're using the same python version

**Instructions**
1. Install all the packages you want by
   * `pip install --target ./python pkg_name`
   * e.g. `pip install --target ./python requests`
2. Add any additional code you want to be importable into the `python` folder
   * e.g. `importable_file1.py1` has `def hello_world():print("Hello")`
   * can then `import importable_file1; hello_world()` in your code.
3. Zip the python folder 
   * Make sure the zipped folder starts with a root `python` folder, then with packages inside
4. Example structure
    ```
    python.zip
    |__ python
        |__ importable_file1.py
        |__ importable_package2
        |__ numpy
        |__ pandas
        |__ ...
     ```
5. Upload zipped file (`python.zip`) to aws (can be named anything)
