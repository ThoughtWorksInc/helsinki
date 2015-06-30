#!/bin/bash
sudo docker stop helsinki || echo "Failed to stop helsinki container"
sudo docker rm helsinki || echo "Failed to remove helsinki"
sudo docker run -d -v /var/helsinki/dist:/var/helsinki/dist --name helsinki-mailshot --link mongo:mongo --link elasticsearch:elasticsearch  python:2.7 bash -c 'pip install /var/helsinki/dist/helsinki-0.0.1.tar.gz && helsinki --mailshot'
