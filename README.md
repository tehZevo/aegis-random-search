# Aegis random search node
a docker container that launches docker containers. tries hyperparameters; collects metrics

*Docker optimizapus,* ***BLAH!***

## TODO
- document requirements for target container (env vars are hyperparameters, last line of output is json that contains metrics; also if you need an env var to be set in all containers, just pass a list with ONLY ONE value)
- support gpu access and other `.run` args
- document request/response and env vars
- integrate with aegis-tensorboard-logger
- catch uncaught exceptions and sigint/sigterm to "clean up"
  - send sigint/sigterm to child containers (docker compose down?) on exception or sigint/sigterm
