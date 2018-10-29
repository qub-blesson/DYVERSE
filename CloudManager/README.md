# Cloud Manager for Face Detection (FD)
This is the Cloud manager for the real-time face detection application.

## Tested Platform
We have tested the Cloud manager on AWS EC2 t2.micro with Ubuntu Server 16.04 LTS.

## Requirement
- [Python](https://www.python.org/)

## How to use
1. Update:
- *EDGE_IP* in requestEdgeService.py & terminateEdgeService.py
2. Make sure Edge Manager is up running
3. Request Edge service:
```
python requestEdgeService.py
```
4. Terminate Edge service:
```
python terminateEdgeService.py
```
