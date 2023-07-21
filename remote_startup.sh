#!/bin/bash

IMAGE=gcr.io/ecomercebackend-393408/cs428-backend:latest

sudo gcloud auth print-access-token | sudo docker login -u oauth2accesstoken \
  --password-stdin  https://us-central1-a-docker.pkg.dev

sudo gcloud auth configure-docker https://us-central1-a-docker.pkg.dev
sudo docker pull $IMAGE

CONTAINER_ID=$(sudo docker ps -qf "name=backend")
if [ ! -z "$CONTAINER_ID" ]; then
  sudo docker stop $CONTAINER_ID
  sudo docker rm -v $CONTAINER_ID
fi

sudo docker run -d -p 8000:8000 --name backend $IMAGE