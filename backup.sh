#!/bin/bash
ssh $REMOTE_USER@$SERVER_IP << EOF
  sudo docker exec -it mongo mongodump --db helsinki --out /data/backup
  sudo tar -zcvf /data/backup/helsinki-backup.tar.gz /data/backup/helsinki
EOF
scp $REMOTE_USER@$SERVER_IP:/data/backup/helsinki-backup.tar.gz helsinki-backup.tar.gz
