ssh $REMOTE_USER@$SERVER_IP "mkdir -p /var/helsinki/dist"
scp dist/* $REMOTE_USER@$SERVER_IP:/var/helsinki/dist
ssh $REMOTE_USER@$SERVER_IP << EOF
  sudo docker stop helsinki || echo "Failed to stop helsinki container"
  sudo docker stop mongo || echo "Failed to stop mongo container"
  sudo docker stop elasticsearch || echo "Failed to stop elasticsearch container"
  sudo docker rm helsinki || echo "Failed to remove helsinki"
  sudo service docker restart
  sudo docker start elasticsearch
  sudo docker start mongo
  sudo docker run -d -v /var/helsinki/dist:/var/helsinki/dist -p 127.0.0.1:5000:5000 --name helsinki --link mongo:mongo --link elasticsearch:elasticsearch  python:2.7 bash -c 'pip install /var/helsinki/dist/helsinki-0.0.1.tar.gz && helsinki --reindex'
EOF
