# Creating a docker image

1) Create a Dockerfile

.. code-block:: dockerfile

    # set base image (host OS)
    # https://hub.docker.com/_/python
    FROM python:3.8-slim

    # set the working directory in the container
    # (creates and cd's into the directory) 
    WORKDIR /code

    # copy the dependencies file to the working directory
    COPY requirements.txt .

    # install dependencies
    RUN pip install -r requirements.txt

    # copy the content of the local src directory to the working directory
    COPY src/ .

    # command to run on container start
    CMD [ "python", "./run.py" ]
    
    
2) Build the image 

.. code-block:: batch
    
    # In the folder, run the command to create the image 
    docker build -t myimage .
    
    # Check its there
    docker image ls
    
3) Run the image

.. code-block:: batch
    docker run myimage
