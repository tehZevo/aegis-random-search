import os
import json
import uuid
import socket
import subprocess
import time
import signal

from python_on_whales import docker, download_binaries
from protopost import protopost_client as ppcl

my_network = None
child_container = None

def cleanup():
  global my_network, child_container
  if my_network is not None:
    my_network.remove()
  if child_container is not None:
    child_container.stop()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

#get env vars from randomsearch
APPLES = os.getenv("APPLES", 0)
BANANAS = os.getenv("BANANAS", 0)

id = uuid.uuid4()
my_network = docker.network.create(id)
this_container_name = socket.gethostname()

#connect this container to the network we just created
#since python on whales doesn't seem to have support for .connect...
#https://docs.docker.com/engine/reference/commandline/network_connect/
print("running network link")
subprocess.run([download_binaries.get_docker_binary_path(), "network", "connect", my_network.name, this_container_name])

#run child container in the network we created
print("building child image")
child_image = docker.build("./child")
print("running child container")
child_container = docker.run(child_image, name=id, detach=True, networks=[my_network], hostname="child", remove=True)

#create protopost function
FRUITINESS = lambda apples, bananas: ppcl(f"http://{id}", {"apples": apples, "bananas": bananas})

#call protopost function
print("calling protopost function")
while True:
  try:
    result = FRUITINESS(APPLES, BANANAS)
    break
  except Exception:
    print("Failed to connect, retrying...")
    time.sleep(1)

cleanup()

#write metrics to stdout
print(json.dumps({"fruitiness":result}))
