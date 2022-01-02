# Aegis random search node
a docker container that launches docker containers. tries hyperparameters; collects metrics

*Docker optimizapus,* ***BLAH!***

## Environment
- `NUM_WORKERS` - number of simultaneous stacks to deploy (defaults to 4)
- `DELAY` - number of seconds to wait after every run (defaults to 0)
- `BUILD_CONTEXT` - `docker-compose.yml` location
- `PORT` - the port to listen on (defaults to 80)
- `PARAMS` - a YAML dictionary-of-lists representing the hyperparameters to try (see `./docker-compose.yml` for an example)

## Usage
### `PARAMS` dictionary
In the compose file, the `|` character can be used to add a block multiline string literal (perfect for representing YAML in YAML):
```yaml
PARAMS: |
  APPLES: [1, 2, 3]
  BANANAS: [2, 3, 4]
```
In this case for each spawned stack, a random value for APPLES will be chosen (e.g. 2), and a random value for BANANAS will be chosen (e.g. 4). These values of APPLES and BANANAS will be passed to a .env file for the target compose file.

### Target compose file
The target compose file should have a service named `main`. This is the service that will be `docker-compose run`'d (its dependencies will be started as well)

### Metrics response
The last line of stdout from the `main` service is parsed as json and interpreted as the dictionary of metrics for that set of hyperparameters.

## TODO
- support gpu access and other `.run` args
- document request/response
- integrate with aegis-tensorboard-logger
- catch uncaught exceptions and sigint/sigterm to "clean up"
  - send sigint/sigterm to child containers (docker compose down?) on exception or sigint/sigterm
- test dependencies starting
