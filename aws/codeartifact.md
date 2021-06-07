# Creating pypi using AWS CodeArtifact

## Creating the project

1) Create the requirements.txt
2) Create the setup.py file
3) Run `python3 setup.py sdist` - create a compressed tarball for source distribution
4) pip install twine
5) Log in to twine with aws
   ```
   export AWS_DEFAULT_PROFILE="abc-production"
   export AWS_DEFAULT_REGION="eu-west-1"
   
   aws codeartifact login --tool twine --domain company-name-production-pypi --domain-owner 123456789 --repository company-name-pypi-repo
   ```
6) Upload with twine 
   ```
   twine upload --repository codeartifact dist/company-name-test-project-0.2.0.tar.gz
   ```
7) Login with pip
   ```
   aws codeartifact login --tool pip --domain company-name-production-pypi --domain-owner 123456789 --repository company-name-pypi-repo
   ``` 
