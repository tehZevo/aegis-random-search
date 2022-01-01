import os, random, time, threading, json, contextlib, uuid
import concurrent.futures

import yaml
from python_on_whales import docker, DockerClient
from protopost import ProtoPost

PORT = int(os.getenv("PORT", 80))
NUM_WORKERS = int(os.getenv("NUM_WORKERS", 4))
DELAY = float(os.getenv("DELAY", 0))
PARAMS = os.getenv("PARAMS", {})
PARAMS = yaml.safe_load(PARAMS)
print(PARAMS)

BUILD_CONTEXT = os.getenv("BUILD_CONTEXT", "/target")

def run(**kwargs):
  #create project name
  id = uuid.uuid4()
  #create env file from kwargs
  env_filename = f"{id}.env"
  with open(env_filename, "w") as f:
    s = "\n".join([f"{k}={v}" for k, v in kwargs.items()])
    f.write(s)

  #create new docker client
  client = DockerClient(
    compose_files=[os.path.join(BUILD_CONTEXT, "docker-compose.yml")],
    compose_env_file=env_filename,
    compose_project_name=f"aegis-random-search-{id}"
  )

  #compose run (stream=True to output lines)
  #TODO: suppress output
  #TODO: cleanup
  # with contextlib.redirect_stdout(None):
  output = client.compose.run("main", tty=False, stream=True)
  output = [s[1] for s in output if s[0] == "stdout"] #grab all stdout lines

  #last line of stdout is the result (json)
  metrics = output[-1]
  metrics = json.loads(metrics)

  #remove containers
  client.compose.down(volumes=True)

  #delete env file
  os.remove(env_filename)

  time.sleep(DELAY)
  return metrics

def choose_params(param_options):
  params = {}
  for k, v in param_options.items():
    params[k] = random.choice(v)
  return params


results = []
counter = 0
#create thread pool executor
#run loop in a separate thread (that starts tasks, checks for empty slots, and updates db)
def thread_cute():
  #   #TODO: catch errors (should we log these? if so, probably in a separate file/table/whatever)
  global counter
  with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = []
    while True:
      #fill up pool with random parameter-running instances
      while len(futures) < NUM_WORKERS:
        params = choose_params(PARAMS)
        future = executor.submit(run, **params)
        futures.append([params, future])

      #wait for at least one to finish
      try:
        concurrent.futures.wait([f for _, f in futures], return_when=concurrent.futures.FIRST_COMPLETED)
      except Error as e:
        print(e)
        continue

      #for each future that completes, append [params, metrics] to results
      for params, future in futures:
        if future.done():
          metrics = future.result()
          counter += 1
          print(counter, params, metrics)
          results.append([params, metrics])

      #remove done futures
      futures = [[p, f] for p, f in futures if not f.done()]


threading.Thread(target=thread_cute, daemon=True).start()

#TODO: add method for filtering by only including samples with a certain hparm combo
#potentially add method for adding/removing hyperparameters live? (might REALLY mess with graphing)
routes = {
  "": lambda data: results
}

ProtoPost(routes).start(PORT)
