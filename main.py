import os, random, time, threading, json, contextlib
import concurrent.futures

import yaml
from tinydb import TinyDB, Query
from python_on_whales import docker
from protopost import ProtoPost

PORT = int(os.getenv("PORT", 80))
PASS_SOCKET = os.getenv("PASS_SOCKET", "false") == "true"
NUM_WORKERS = int(os.getenv("NUM_WORKERS", 4))
DELAY = float(os.getenv("DELAY", 0))
PARAMS = os.getenv("PARAMS", {})
PARAMS = yaml.safe_load(PARAMS)
print(PARAMS)

DB_PATH = os.getenv("DB_PATH", "./db.json")

BUILD_CONTEXT = os.getenv("BUILD_CONTEXT", "/target")

#build image
image = docker.build(BUILD_CONTEXT)

db = TinyDB(DB_PATH)

def run(**kwargs):
  vols = []
  if PASS_SOCKET:
    vols.append(("/var/run/docker.sock", "/var/run/docker.sock"))

  output = docker.run(image, remove=True, envs=kwargs, volumes=vols)

  #last line of stdout is the result (json)
  metrics = output.split("\n")[-1]
  metrics = json.loads(metrics)
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
          db.insert({"params":params, "metrics":metrics})

      #remove done futures
      futures = [[p, f] for p, f in futures if not f.done()]


threading.Thread(target=thread_cute, daemon=True).start()

#TODO: add method for filtering by only including samples with a certain hparm combo
#potentially add method for adding/removing hyperparameters live? (might REALLY mess with graphing)
routes = {
  "": lambda data: results
}

ProtoPost(routes).start(PORT)
