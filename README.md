# Django Tasks Project
This Django project allows users to create tasks, view them, and mark them as completed. It is built using Docker and Docker Compose, and includes a suite of tests and linters that can be run using the tox command.

## Prerequisites
- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docker-docs.netlify.app/compose/install/#install-compose)
- [Tox](https://pypi.org/project/tox/#description) (optional, for running tests and linters)

## Running the Project
Build the Docker images and run the containers:

`docker-compose up -d --build`

After running the container, you can access the application in [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

To run the tests and linters execute:

`tox`
