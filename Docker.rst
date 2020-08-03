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
    
    ## NOTE: if you want print commands to show, then you can either:
    # 1) add `-u` - it will display "unbuffered" output
    CMD [ "python", "-u", "./run.py"]

    # 2)  set the environment variable PYTHONUNBUFFERED=0
    ENV PYTHONUNBUFFERED=0
    CMD [ "python", "./run.py" ]

    
    
2) Build the image 

.. code-block:: bash
    
    # In the folder, run the command to create the image 
    # -t = tag, so give it a unique name (otherwise it will overwrite the old names)
    docker build -t myimage .
    
    # Check its there
    docker image ls
    
3) Run the image

.. code-block:: bash

    docker run myimage

4) Freeze into the image (To debug)

.. code-block:: bash

    docker run -it myimage bash
    docker run -it myimage /bin/bash
