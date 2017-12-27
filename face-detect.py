import time
import picamera
import io
import cv2
import numpy
import datetime
import base64

camera = picamera.PiCamera()

def detectionFace() :
    time.sleep(2)
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
    image = cv2.imdecode(buff, 1)
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) > 0 :
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imwrite('result.jpg',image)
        stopCamera()
        with open("result.jpg", "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
            print(str)
    else :
        startCamera()
        
def startCamera() :
    camera.resolution = (640, 480)
    camera.start_preview(fullscreen=False, window=(100,100,400,400))
    detectionFace()

def stopCamera() :
    camera.stop_preview()

def captureImage() :
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
    print('Capture image successfully')

if __name__ == "__main__":
    startCamera()
    while True :
        try:
            command = str(raw_input('command : '))
            if command == 'stop' :
                print('Stop Camera')
                stopCamera()
            elif command == 'start' :
                print('Start Camera')
                startCamera()
            elif command == 'capture' :
                captureImage()
        except ValueError:
            print "Not a string"
