### useful commands

1. sudo docker stack rm app_name
2. cd autoscaler
3. sudo docker build -t auto:1 .
4. sudo docker stack deploy --compose-file docker-compose.yml app_name
5. sudo docker service logs app_name_autoscaler
6. sudo docker service logs app_name_web
