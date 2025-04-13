# HOW TO RUN

In VScode use tasks to
* Run and Debug
  * `Django makemigrations`
  * `Django migrate`
  * `Django createsuperuser`
  * `Django runserver`


### Building and running the Docker container

A sample Dockerfile is provided which will build and run the application.

It mounts one Docker volume on /app/storage for local file storage, and will connect to an SQL database specified with the environment variable "DATABASE_URL".

If "DATABASE_URL" is blank, it will default to an SQLite database on the /app/storage volume.

Install [Docker](https://www.docker.com/) on your system.

To build:
`docker build . -t myapp`

To create a persistent storage volume:
`docker volume create myapp-storage`

To run the container:
`docker run -ti -v myapp-storage:/app/storage -p 8000:8000 myapp`

To delete the persistent volume (i.e. any stored files and test databases)
`docker volume rm myapp-storage`
