import docker
from flask import Flask
import requests
import time
app = Flask(__name__)

SERVICE_NAME = "app_name_web"


import time

class DockerController:
    def __init__(self, service_name):
        self.service_name = service_name
        self.client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        self.service = self.client.services.get(self.service_name)
        print("Getting replicas")
        self.number_of_replicas = self.get_number_of_replicas()
        print("Got replicas")

    def decrement_num_reps(self):
        if self.number_of_replicas > 1:
          print("Decrementing number of replicas")
          self.service.reload()
          self.service.update(mode={'Replicated': {'Replicas': self.number_of_replicas - 1}})
          self.number_of_replicas = self.number_of_replicas - 1

    def increment_num_reps(self):
        print("Incrementing number of replicas")
        self.service.reload()
        self.service.update(mode={'Replicated': {'Replicas': self.number_of_replicas + 1}})
        self.number_of_replicas = self.number_of_replicas + 1

    def get_number_of_replicas(self):
        return self.service.attrs['Spec']['Mode']['Replicated']['Replicas']

class AverageCalculator:
    def __init__(self, sample_time=15):
        self.sample_time = sample_time
        self.times = []
        self.last_sample_start = time.time()
        self.docker_controller = DockerController(SERVICE_NAME)
        self.response_times_per_replica = []
        self.baseline_average = 1.5
        self.prev_average = 0
        self.num_replicas = self.docker_controller.number_of_replicas

    def is_window_expired(self):
      if time.time() - self.last_sample_start > self.sample_time:
        return True
    
    def get_average(self):
      if self.is_window_expired():
        self.last_sample_start = time.time()
        average = sum(self.times) / len(self.times)
        self.times = []
        if (average < self.baseline_average):
          self.docker_controller.decrement_num_reps()
        elif (average > self.baseline_average):
          self.docker_controller.increment_num_reps()
        self.prev_average = average

    def update(self, process_variable):
      self.times.append(process_variable)
      self.response_times_per_replica.append(process_variable/self.num_replicas)
      self.get_average()
        
averageCalculator = AverageCalculator()

@app.route('/')
def hello():
  start_time = time.time()
  r = requests.get('http://web:8000')
  end_time = time.time()
  res_time = end_time - start_time
  averageCalculator.update(res_time)
  print("Respone time: ", res_time)
  return r.text

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=True)


           