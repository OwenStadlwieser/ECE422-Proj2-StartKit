import docker
from flask import Flask
import requests
import time
app = Flask(__name__)

SERVICE_NAME = "web_app"


import time

class DockerController:
    def __init__(self, service_name):
        self.service_name = service_name
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.service = self.client.services.get(self.service_name)
        self.number_of_replicas = self.get_number_of_replicas()

    def decrement_num_reps(self):
        if self.get_number_of_replicas() > 1:
          print("Decrementing number of replicas")
          self.service.update(mode={'Replicated': {'Replicas': self.get_number_of_replicas() - 1}})

    def increment_num_reps(self):
        print("Incrementing number of replicas")
        self.service.update(mode={'Replicated': {'Replicas': self.get_number_of_replicas() + 1}})

    def get_number_of_replicas(self):
        return self.service.attrs['Spec']['Mode']['Replicated']['Replicas']

class AverageCalculator:
    def __init__(self, sample_time=15):
        self.sample_time = sample_time
        self.times = []
        self.last_sample_start = time.time()
        self.response_times_per_replica = []
        self.prev_average = 0.148

    def is_window_expired(self):
      if time.time() - self.last_sample_start > self.sample_time:
        return True

    def get_average(self):
      if self.is_window_expired():
        self.last_sample_start = time.time()
        average = sum(self.response_times_per_replica) / len(self.response_times_per_replica)
        self.times = []
        # if (average < self.prev_average):
          # self.docker_controller.decrement_num_reps()
        # elif (average > self.prev_average):
          # self.docker_controller.increment_num_reps()
        self.prev_average = average

    def update(self, process_variable):
      self.times.append(process_variable)
      # self.response_times_per_replica.append(process_variable/ self.docker_controller.get_number_of_replicas())
      self.get_average()


if __name__ == "__main__":
    averageCalc = AverageCalculator()
    averageCalc.update(0.1)