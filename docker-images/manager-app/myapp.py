import random
import time
import pandas
import statistics
import docker
import requests

IMAGE_NAME = "web_app"
LOWER_BOUND = 20
HIGHER_BOUND = 50
def calc_response_time():
    pass

def create_service():
    docker.service.create(IMAGE_NAME, )

def set_number_of_replicas(num_reps: int):
    
    docker.service.update(mode={'Replicated': {'Replicas': new_replicas}}).create()



if __name__ == "__main__":
   while(True):
      res_time = calc_response_time()
      if (res_time < LOWER_BOUND):
        pass
      elif (res_time > HIGHER_BOUND):
        pass   
      else: 
        pass
           