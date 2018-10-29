import socket
import sys
import os

def send_request():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((EDGE_IP, PORT))
    
    s.send("terminate %s" % App)
    response = s.recv(1024)
	print response
    s.close()


if __name__ == "__main__":
	PORT = 2221
    EDGE_IP = '90.214.69.151'       # Change this to Edge IP
	App = sys.argv[1]
	send_request()
