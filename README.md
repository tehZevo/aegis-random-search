# Aegis random search node
a docker container that launches docker containers which potentially launch other docker containers. try hyperparameters; collect metrics

*Docker optimizapus,* ***BLAH!***

## Notes
- BUILD_CONTEXT can be a git url, so optimization can be performed on dockerfiles in git repos
- random search passes /var/run/docker.sock to the target container

## TODO
- document requirements for target container (env vars are hyperparameters, last line of output is json that contains metrics; also if you need an env var to be set in all containers, just pass a list with ONLY ONE value)
- wrap non-list hyperparameters in a list? or make separate "defaults" env var object to pass verbatim to target container? idk?
- how to handle gpu access and other .run args?
  - honestly, the best way to handle this may be to make a proxy container that uses python_on_whales or other language library to fully control the target container
- save results to file/database (no need if tensorboard integration!)
- document request/response and env vars
- potential integration with tensorboard (https://www.tensorflow.org/tensorboard/hyperparameter_tuning_with_hparams; may make downloading csv/json data easy)
  - integrate with aegis-tensorboard-logger
- suppress output of other containers
- catch uncaught exceptions and sigint/sigterm to "clean up"
- predownload docker cli (initialize python_on_whales)
- stop runner containers on sigint/sigterm
### Future: compose files
Optimizing on compose files may be difficult.. with python on whales, there doesn't seem to be a way to provide an env *dict* (files, yes. dict, no.) so for now, focus on providing an example of containers that start other containers (incl. clean up process)
