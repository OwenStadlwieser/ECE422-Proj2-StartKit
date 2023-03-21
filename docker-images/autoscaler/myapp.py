import docker
from flask import Flask
import requests
import time
app = Flask(__name__)

IMAGE_NAME = "web_app"
LOWER_BOUND = 20
HIGHER_BOUND = 50
def calc_response_time():
    pass

# def create_service():
#     docker.service.create(IMAGE_NAME, )

# def set_number_of_replicas(num_reps: int):
    
#     docker.service.update(mode={'Replicated': {'Replicas': new_replicas}}).create()


@app.route('/')
def hello():
  start_time = time.time()
  r = requests.get('http://web:8000')
  end_time = time.time()
  res_time = start_time - end_time
  if (res_time < LOWER_BOUND):
    pass
  elif (res_time > HIGHER_BOUND):
    pass   
  else: 
    pass
  print("Respone time: ", res_time)
  return r.text

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=True)


           