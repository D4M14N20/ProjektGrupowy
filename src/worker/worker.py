import docker
import shutil
import time
import json
import os
import subprocess

#configuration

total_time = time.time()

client = docker.from_env()
volume = f"{ os.environ.get('WORKER_SHARED_VOLUME') }"
subprocess.run("chmod -R 777 /data", shell=True, check=True)

#compilation

if compile:
    print("Running compilation container...")
    start_time = time.time()
    comp_container = client.containers.run(
        "comp",
        name="comp-container",
        remove=True,
        environment={"INPUT":"/data/comp-in", "OUTPUT":"/data/comp-out"},
        security_opt=["no-new-privileges"],
        volumes={
            volume: {"bind": "/data", "mode": "rw"},
        },
    )

    print(f"Compilation time: {round(time.time() - start_time, 2)} seconds")
    shutil.copy(os.path.join("/data/comp-out", "program"), "/data/comp-in")

#execution

print("Starting execution container...")
start_time = time.time()
exec_container = client.containers.run(
    "exec",
    name="exec-container",
    remove=True,
    environment={"INPUT":"/data/exec-in", "OUTPUT":"/data/exec-out"},
    security_opt=["no-new-privileges"],
    volumes={
        volume: {"bind": "/data", "mode": "rw"},
    }
)
print(f"Execution time: {round(time.time() - start_time, 2)} seconds")

#printing resoults

for j in range(20):
    try:
        with open(f"/data/exec-out/{j}.resource.json", "r") as file:
            data = json.load(file)
            print(f":{j} -> {round(data[0], 2)}s")
    except Exception as e:
        pass

print(f"Total time: {round(time.time() - total_time, 2)} seconds")
