from socket import *
import cv2

host = "0.0.0.0"        # This is to use the public IP of AWS EC2 instance
port = 4097
buf = 1024
addr = (host, port)
fName = 'greyImg.jpg'
timeOut = 0.05

def handle():
    print "Cloud server running..."
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    
    while True:
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(addr)

        data, address = s.recvfrom(buf)
        f = open(data, 'wb')

        data, address = s.recvfrom(buf)

        try:
            while(data):
                f.write(data)
                s.settimeout(timeOut)
                data, address = s.recvfrom(buf)
        except timeout:
            f.close()
            s.close()
        
        # Detect faces
        print "Detecting face..."
        image = cv2.imread(fName)
        faces = faceCascade.detectMultiScale(
                                             image,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(30, 30)
                                             )
        print "Faces: ", faces
        print "End time: ", time()


if __name__ == '__main__':
    handle()
