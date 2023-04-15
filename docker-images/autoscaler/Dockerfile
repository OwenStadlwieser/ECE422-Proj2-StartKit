#!/usr/bin/env sh
FROM python:3.6.9
ADD . /code
WORKDIR /code
RUN python3 -m pip install -r requirements.txt
CMD ["python", "myapp.py"]
