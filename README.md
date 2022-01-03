# Aegis random search node
a docker container that launches docker containers. tries hyperparameters; collects metrics

*Docker optimizapus,* ***BLAH!***

## Environment
- `EXPERIMENT_NAME` - name of the experiment; will be used in compose project name and TensorBoard hyperparameter logging (if enabled); (defaults to "experiment")
- `NUM_WORKERS` - number of simultaneous stacks to deploy (defaults to 4)
- `DELAY` - number of seconds to wait after every run (defaults to 0)
- `BUILD_CONTEXT` - `docker-compose.yml` location
- `TENSORBOARD_LOGGER_URL` - logger of an [aegis-tensorboard](https://github.com/tehZevo/aegis-tensorboard) instance to log hyperparameters and metrics to; defaults to None (disabled)
- `PARAMS` - a YAML dictionary-of-lists representing the hyperparameters to try (see `./docker-compose.yml` for an example)
- `PORT` - the port to listen on (defaults to 80)

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

### MetaHyperParameters
In cases where related parameters are required, a list of dicts can be provided:
```yaml
MHP: [{"A":1, "B":10}, {"A":2, "B":20}]
```
Here, either A as 1 and B as 10 will be selected OR A as 2 and B as 20 will be selected. A and B will be treated as their own hyperparameters when being passed to the target stack and when logging (the term `MHP` will not appear).

## TODO
- support gpu access and other `.run` args
- document request/response
- integrate with aegis-tensorboard-logger
- catch uncaught exceptions and sigint/sigterm to "clean up"
  - send sigint/sigterm to child containers (docker compose down?) on exception or sigint/sigterm
- test dependencies starting
- consider bayesian optimization
