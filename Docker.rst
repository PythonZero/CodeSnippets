Creating a docker image
###########################

- Dockerfiles work by going instructions one by one. It caches it, and stores each instruction.
- Only if there's a change in an instruction, will it be re-run
- So, if e.g. step 3 is copy copy requirements file. If the file hasn't changed it will skip
- Then step 4 (run the pip install reqs) will also skip, because nothing's changed
- Thats why, its better to install the reqs first, THEN copy all the files, so changing one file won't
  mean that you have to re-install the requirements each time.

1) Create a Dockerfile

.. code-block:: dockerfile

    # set base image (host OS)
    # https://hub.docker.com/_/python
    FROM python:3.8-slim

    # set the working directory in the container
    # (creates and cd's into the directory) 
    WORKDIR /code

    # copy the dependencies file to the working directory 
    # we do this separately, so that when you re-create the image, it can skip the
    # re-installing of requirements each time, and uses the old version (unless the reqs change)
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
    
    # In the folder with the Dockerfile, run the command to create the image 
    # -t = tag, so give it a unique name (otherwise it will overwrite the old names)
    docker build -t myimage .
    
    # Check its there
    docker image ls
    
3) Run the image

.. code-block:: bash

    docker run myimage

4) Freeze into the image (To debug)

.. code-block:: bash
    
    # -it = --interactive and --tty (tty is essentially a text input output environment aka shell)
    docker run -it myimage bash
    docker run -it myimage /bin/bash
    
    # Build and run together
    docker build -t myimage . && docker run -it myimage bash
        

Images vs Containers
#########################

- Images contain the instructions to create the virtual machine.
- Containers are created when you run the image (and close, when finished running)

1) Run a continuous process (i.e. a webserver, or a bash shell) - this creates a container that remains running
    
.. code-block:: bash
  
  #  -it = --interactiv and -d = detached,
  docker run -itd myimage bash

2) Show the container 

.. code-block:: bash

   # Either ls or ps
   docker container ls
   docker ps
   # See all containers (including stopped ones)
   docker ps -a
   
3) Attach into the container

.. code-block::

   docker attach <CONTAINER ID from step 2 - you can type only the first few characters> 
   
Clearing Containers / Images
###############################

- Even after closing a container, it still exists in the background

.. code-block:: 
     
   # List all containers (Including stopped ones)
   docker ps -a -q
   
   # Stop/Kill all containers (Kill = forced version of stop)
   docker stop $(docker ps -a -q)
   docker kill $(docker ps -a -q)
   
   # Remove all containers
   docker rm $(docker ps -a -q)
   
.. code-block:: 
  
  # Remove all images that don't have  a container
  docker image prune


Docker Compose
#################################

- Create a ``docker-compose.yaml`` file.
- Has the rules for how to deploy the server (can deploy multiple servers & how they interact)

.. code-block:: Docker

  version: '3'                   # The DockerCompose Version we're using
  services:
    sval-web:                    # Service 1's container name
      build: .                   # Use the Dockerfile in this folder
      ports:
        - "5000:5000"            # Bind these ports

    redisImage:                  # (Optional, a second Service)
      image: "redis:alpine"      # no Dockefile
      
Making Docker Compose work with Pycharm (Windows)
+++++++++++++++++++++++++++++++++++++++++++++++++
1) Deleting the existing image / Re-running the image
2) In docker for windows settings
  a) In General -> Expose daemon on tcp://localhost:2375 without TLS
  b) In Resources -> File Sharing -> Added the directory for pycharm (or just add the whole C:\ drive)
