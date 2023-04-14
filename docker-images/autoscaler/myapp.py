import docker
from flask import Flask
import requests
import time
from threading import Thread
from time import sleep
import plotly.graph_objects as go

app = Flask(__name__)

SERVICE_NAME = "app_name_web"

epsilon = 5

delta_epsilon = 0.2
print("In app")

class DockerController:
    def __init__(self, service_name):
        self.service_name = service_name
        self.client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        # update_config = docker.types.UpdateConfig(
        #     parallelism=2,
        #     delay=10
        # )
        # print("Here")
        # try:
        #   self.service.update(update_config=update_config)
        # except Exception as e:
        #   print(e)
        print("Getting replicas")
        self.number_of_replicas = self.get_number_of_replicas()
        print("Got replicas")

    def decrement_num_reps(self, reset = False):
        if self.number_of_replicas > 1:
          num_reps = 1 if reset else self.number_of_replicas - 1
          print("Decrementing number of replicas")
          service = self.client.services.get(self.service_name)
          service.scale(num_reps)
          self.number_of_replicas = num_reps

    def increment_num_reps(self, factor = 1):
        print("Incrementing number of replicas")
        service = self.client.services.get(self.service_name)
        self.number_of_replicas = self.number_of_replicas + factor
        service.scale(self.number_of_replicas)

    def get_number_of_replicas(self):
        service = self.client.services.get(self.service_name)
        return service.attrs['Spec']['Mode']['Replicated']['Replicas']

class AverageCalculator:
    def __init__(self, sample_time=15):
        self.sample_time = sample_time
        self.times = []
        self.last_sample_start = time.time()
        self.docker_controller = DockerController(SERVICE_NAME)
        self.response_times_per_replica = []
        self.baseline_average = 1.6
        self.prev_average = 0
        self.num_replicas = self.docker_controller.number_of_replicas

    def is_window_expired(self):
      if (time.time() - self.last_sample_start) > self.sample_time:
        return True
    
    def get_average(self):
      self.last_sample_start = time.time()
      print("Times")
      print(self.times)
      print(self.response_times_per_replica)
      if self.times and len(self.times) > 0:
        average = sum(self.times) / len(self.times)
        self.times = []
        self.response_times_per_replica = []
        if (average < self.baseline_average or average < ( self.prev_average - epsilon )):
          self.docker_controller.decrement_num_reps()
        elif (average > self.baseline_average and average > ( self.prev_average + delta_epsilon )):
          factor = int(average // self.baseline_average)
          self.docker_controller.increment_num_reps(factor)
        self.prev_average = average
      else:
        self.docker_controller.decrement_num_reps(True)
    def update(self, process_variable):
      print("Update")
      self.times.append(process_variable)
      self.response_times_per_replica.append(process_variable/self.num_replicas)


class GraphDrawer:
  def __init__(self):
    self.docker_controller = DockerController(SERVICE_NAME)
    self.amount_replicas = []
  def draw_graph(self):
    self.amount_replicas.append({ 'num_replicas': self.docker_controller.get_number_of_replicas(), 'time': time.time() })
    x_values = [item['time'] for item in self.amount_replicas]
    y_values = [item['num_replicas'] for item in self.amount_replicas]

    # Create line chart
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='lines'))

    # Add labels and title
    fig.update_layout(xaxis_title='Time', yaxis_title='Number of Replicas', title='Replica Count over Time')

    # Save chart to file
    fig.write_image('replicas.png')

averageCalculator = AverageCalculator()

def draw_loop():
  graphDrawer = GraphDrawer()
  while True:
    print("Drawing")
    graphDrawer.draw_graph()
    sleep(10)
def check_loop():
  while True:
    print("Getting average")
    averageCalculator.get_average()
    sleep(10)
    


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
  Thread(target=check_loop, daemon=True).start()
  Thread(target=draw_loop, daemon=True).start()
  app.run(host="0.0.0.0", port=8000, debug=True)


           