#!bin/bash

EDGE_IP=$1
EDGE_PORT=$2 # This is the last port in request.txt, which is updated when Edge service is setup

ssh -i edge.key root@$EDGE_IP -p $PORT
apk add python py-pillow
git clone https://github.com/NanWang0024/FaceDetection-EdgeServer.git fd-edgeserver
cd fd-edgeserver

# Launch server
nohup python 2grey.py > serverLog &
