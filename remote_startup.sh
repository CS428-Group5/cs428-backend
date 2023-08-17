#!/bin/bash

sudo snap install docker

POSTGRES_CONTAINER_ID=$(sudo docker ps -qf "name=mentoree-db")
if [ -z "$POSTGRES_CONTAINER_ID" ]; then
  sudo docker run -dit --name mentoree-db -e POSTGRES_DB=mentoree -e POSTGRES_USER=ecomerce -e POSTGRES_PASSWORD=1234 -p 49153:5432 postgres:latest
fi

IMAGE=gcr.io/ecomercebackend-393408/cs428-backend:latest

sudo gcloud auth print-access-token | sudo docker login -u oauth2accesstoken \
  --password-stdin  https://gcr.io

sudo gcloud auth configure-docker https://gcr.io
sudo docker pull $IMAGE

CONTAINER_ID=$(sudo docker ps -qf "name=backend")
if [ ! -z "$CONTAINER_ID" ]; then
  sudo docker stop $CONTAINER_ID
  sudo docker rm -v $CONTAINER_ID
fi

sudo docker run -d -p 8000:8000 --name backend $IMAGE