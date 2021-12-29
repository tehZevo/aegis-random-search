# Aegis random search node
a docker container that launches docker containers which potentially launch other docker containers. try hyperparameters; collect metrics

*Docker optimizapus,* ***BLAH!***

## TODO
- note that BUILD_CONTEXT can be a git url eg: https://github.com/tehzevo/aegis-discord.git (https://docs.docker.com/engine/reference/commandline/build/)
- document requirements for target container (env vars are hyperparameters, last line of output is json that contains metrics; also if you need an env var to be set in all containers, just pass a list with ONLY ONE value)
- parse non-list params as a list, or make separate env var object to pass verbatim to target container? idk?
- how to handle gpu access and other .run args?
  - honestly, the best way to handle this may be to make a proxy container that uses python_on_whales or other language library to fully control the target container
- save results to file/database (no need if tensorboard integration!)
- document request/response and env vars
- potential integration with tensorboard (https://www.tensorflow.org/tensorboard/hyperparameter_tuning_with_hparams; may make downloading csv/json data easy)
  - integrate with aegis-tensorboard-logger
- perhaps work on compose files instead of containers (but then how do we track the "main" result)
  - probably cant trust stdout of `docker-compose up` (unless logging: driver: "none"?)
  - container communication:
    - file IO: create global docker volume with compose and env var name like ${AEGIS_RS_23749234}
    - network IO: create network with compose and env var name as above
      - this allows containers to talk to eachother without rewriting their urls
    - network IO to randomsearch's network: join networks? (names must be unique)
