#!/bin/bash

sudo snap install docker

POSTGRES_CONTAINER_NAME="mentoree-db"
if ! (sudo docker ps | grep -q "$POSTGRES_CONTAINER_NAME") && ! (sudo docker ps -a | grep -q "$POSTGRES_CONTAINER_NAME"); then
  sudo docker run -dit --name mentoree-db -e POSTGRES_DB=mentoree -e POSTGRES_USER=ecomerce -e POSTGRES_PASSWORD=1234 -p 49153:5432 postgres:latest
  echo "Do not have the database ... going to create a new one"
elif ! (sudo docker ps | grep -q "$POSTGRES_CONTAINER_NAME"); then
  echo "Database is running in the background..."
  sudo docker start "$POSTGRES_CONTAINER_NAME"
fi

IMAGE=gcr.io/ecomercebackend-393408/cs428-backend:latest

sudo gcloud auth print-access-token | sudo docker login -u oauth2accesstoken \
  --password-stdin  https://gcr.io

sudo gcloud auth configure-docker https://gcr.io
sudo docker pull $IMAGE

WEBSERVER_CONTAINER="backend"
if sudo docker ps | grep -q "$WEBSERVER_CONTAINER"; then
  echo "The container is running in the foreground"
  sudo docker stop "$WEBSERVER_CONTAINER"
fi

if sudo docker ps -a | grep -q "$WEBSERVER_CONTAINER"; then
  echo "The container is running in the background"
  sudo docker rm -v "$WEBSERVER_CONTAINER"
fi

sudo docker run -d -p 8000:8000 --name backend $IMAGE