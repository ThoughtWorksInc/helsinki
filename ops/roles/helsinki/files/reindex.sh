#!/bin/bash
sudo docker run -v /var/helsinki/dist:/var/helsinki/dist --name helsinki_reindex --link elasticsearch:elasticsearch python:2.7 bash -c 'pip install /var/helsinki/dist/helsinki-0.0.1.tar.gz && helsinki --reindex'
sudo docker rm helsinki_reindex
