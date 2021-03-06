#!/bin/bash
ssh $REMOTE_USER@$SERVER_IP "mkdir -p /var/helsinki/dist"
ssh $REMOTE_USER@$SERVER_IP "mkdir -p /var/helsinki/config"
scp dist/* $REMOTE_USER@$SERVER_IP:/var/helsinki/dist
scp config.env $REMOTE_USER@$SERVER_IP:/var/helsinki/config
ssh $REMOTE_USER@$SERVER_IP << EOF
  sudo docker stop helsinki || echo "Failed to stop helsinki container"
  sudo docker rm helsinki || echo "Failed to remove helsinki"
  sudo docker run -d -v /var/helsinki/dist:/var/helsinki/dist -p 127.0.0.1:5000:5000 --name helsinki --link mongo:mongo --link elasticsearch:elasticsearch -e "BASE_URL=https://decisions.dcentproject.eu" --env-file=/var/helsinki/config/config.env python:2.7 bash -c 'pip install /var/helsinki/dist/helsinki-0.0.1.tar.gz && helsinki --reindex && helsinki'
EOF
