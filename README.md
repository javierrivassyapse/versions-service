# versions-service

A new service for displaying the services version deployed in the Syapse environments.

This service is owned and managed by Syapse Engineering


## Quickstart

To get up and running, all you'll need to do is run `bin/setup`.

This will create a Docker-based development environment and start your service.

The Docker environment will pick up changes to your code as you make them.

Your service will be available on:

  * http://localhost:18663/v1/ui/

You can access your PostgreSQL database via pgweb at:

  * http://localhost:18664/


## Useful Commands

The following commands may come in handy as you develop.

### `bin/aws COMMAND`

The `bin/aws` command will let you run an AWS command against LocalStack (the container that emulates AWS services).

#### Examples

* Create a Kinesis stream: `bin/aws kinesis create-stream --stream-name my-stream --shard-count 1`
* List available Kinesis streams: `bin/aws kinesis list-streams`

### `bin/exec COMMAND`

The `bin/exec` command will let you run a process inside of the running service container.

#### Examples

* Get an interactive shell: `bin/exec sh`
* Run a flask command: `bin/exec flask urls`

This is equivalent to `docker-compose exec COMMAND`

### `bin/logs`

The `bin/logs` command will display logs from your running containers.

#### Examples

* Get logs for all containers: `bin/logs`
* Follow logs for all containers: `bin/logs -f`
* Follow logs for the service container: `bin/logs -f versions-service`

This is equivalent to `docker-compose logs`

### `bin/nuke`

The `bin/nuke` command will destroy the Docker environment entirely. Useful for troubleshooting environment issues.

This is equivalent to `docker-compose down --rmi all --volumes --remove-orphans`

### `bin/pytest`

The `bin/pytest` command will run the test suite.

### `bin/reload`

The `bin/reload` command will restart the service container.

This is equivalent to `docker-compose restart versions-service`

### `bin/restart`

The `bin/restart` command will restart all containers (or any containers you specify).

#### Examples

* Restart all containers: `bin/restart`
* Restart postgres: `bin/restart postgres`
* Restart postgres and rabbitmq: `bin/restart postgres rabbitmq`

This is equivalent to `docker-compose restart [container1 [container2]]`

### `bin/setup`

The `bin/setup` command will rebuild the Docker environment and bootstrap the application for development.

### `bin/start`

The `bin/start` command will start all containers (or any containers you specify).

#### Examples

* Start all containers: `bin/start`
* Start postgres: `bin/start postgres`
* Start postgres and rabbitmq: `bin/start postgres rabbitmq`

This is equivalent to `docker-compose start [container1 [container2]]`

### `bin/stop`

The `bin/stop` command will stop all containers (or any containers you specify).

#### Examples

* Stop all containers: `bin/stop`
* Stop postgres: `bin/stop postgres`
* Stop postgres and rabbitmq: `bin/stop postgres rabbitmq`

This is equivalent to `docker-compose stop [container1 [container2]]`


## Deployment

The project contains a Dockerfile that should produce a production-ready container to host the instance.


## The Stack

The following technologies are in use in the project.

* Alembic ([docs](http://alembic.zzzcomputing.com/en/latest/))
* Connexion ([docs](https://connexion.readthedocs.io/en/latest/))
* Docker ([docs](https://docs.docker.com/))
* Flask ([docs](http://flask.pocoo.org/docs/))
* Flask-Cache ([docs](https://pythonhosted.org/Flask-Cache/))
* Flask-Marshmallow ([docs](https://flask-marshmallow.readthedocs.io/en/latest/))
* Gunicorn ([docs](http://docs.gunicorn.org/en/stable/settings.html))
* LocalStack ([docs](https://github.com/localstack/localstack))
* Pynesis ([docs](https://github.com/ticketea/pynesis))
* Python 3.6
* SQLAlchemy ([docs](http://docs.sqlalchemy.org/en/latest/))


## Troubleshooting

### My changes aren't taking effect.

Sometimes the file watcher doesn't pick something up. The fastest solution is to simply restart your container:

```
$ bin/reload  # alternatively: docker-compose restart versions-service
```
