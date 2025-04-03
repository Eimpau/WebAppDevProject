# EEN1037 Example Django Application

## Overview

This example website was produced by following the official Django Documentation tutorial at <https://docs.djangoproject.com/en/5.1/intro/tutorial01/> and extending with our application specific models and HTML templates. Configuration for Visual Studio Code and Docker is also included.

## Customizing

* Use Visual Studio Code "Search and Replace" to replace all instances of "myapp" with "yourwebappname" (e.g. "carsales"). 
* Delete all existing migration files in the `migrations`, e.g.  folders.
* Change the code as you wish


## Developing

### Visual Studio Code launch targets

* Open the project folder in Visual Studio Code
* Press F5 or select `Run and Debug`
* Run the desired launch target, e.g. `Django runserver`


### Generating new database schema migrations

After editing any Model classes in models.py files, you must generate
the SQL schema migrations corresponding to your changes. This can be
done automatically with the `makemigrations` command:

* Run and Debug:
    * `Django makemigrations`

These new files should be saved along with your source code.


### Applying database migrations to the test database

* Run and Debug
  * `Django makemigrations`
  * `Django runserver`
  * `Django migrate`


## Running as a Docker container

A sample Dockerfile is provided which will build and run the application.

It mounts one Docker volume on /app/storage for local file storage, and will connect to an SQL database specified with the environment variable "DATABASE_URL".

If "DATABASE_URL" is blank, it will default to an SQLite database on the /app/storage volume.


### Building and running the Docker container

Install [Docker](https://www.docker.com/) on your system.

You can use Visual Studio Code "Docker" plugin, or the included build tasks (Ctrl+P + "task") or these command line commands:

To build:
```
docker build . -t myapp
```

To create a persistent storage volume:
```
docker volume create myapp-storage
```

To run the container:
```
docker run -ti -v myapp-storage:/app/storage -p 8000:8000 mysite
```

To delete the persistent volume (i.e. any stored files and test databases)
```
docker volume rm myapp-storage
```
