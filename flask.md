# Dockerising Flask

Create the Simple app

```
flask-app
  |__ app.py
  |__ Dockerfile
  |__ requirements.txt
 ```
 
 
app.py
```
#!/usr/bin/env python

import flask
# Create the application.
APP = flask.Flask(__name__)

@APP.route("/")
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template("index.html")

if __name__ == "__main__":
    APP.debug = True
    APP.run(host="0.0.0.0")
```

Dockerfile
```
FROM python:3.8-slim

WORKDIR /backend

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python"]
CMD ["app.py"]
```

```
# Step 1)
docker build -t flask-tutorial:latest .
# Step 2 - MUST use -p (BINDS the port to the local machine)
docker run -d -p 5000:5000 flask-tutorial
```

See [here for explanation of step 2](https://nickjanetakis.com/blog/docker-tip-59-difference-between-exposing-and-publishing-ports#:~:text=You%20can%20expose%20a%20port,%2Dp%2080%3A80%20flag)

