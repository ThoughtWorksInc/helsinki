tar -cvzf $TAR $DIR
ssh $REMOTE_USER@$SERVER_IP "mkdir -p /var/helsinki/dist"
scp dist/* $REMOTE_USER@$SERVER_IP:/var/helsinki/dist
ssh $REMOTE_USER@$SERVER_IP "sudo docker run --rm=true -d -v /var/helsinki/dist:/var/helsinki/dist -p 5000:5000 --name helsinki --link mongo:mongo --link elasticsearch:elasticsearch  python:2.7 bash -c 'pip install /var/helsinki/dist/helsinki-0.0.1.tar.gz && helsinki --reindex'"
