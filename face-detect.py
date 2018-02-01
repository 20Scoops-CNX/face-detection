import time
import picamera
import io
import cv2
import numpy
import datetime
import aws
import os

camera = picamera.PiCamera()
aws_service = aws
date = datetime

def detection_face() :
    time.sleep(2)
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
    image = cv2.imdecode(buff, 1)
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) > 0 :
        date_time = date.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        file_name = str(date_time) + '.jpg'
        cv2.imwrite(os.path.join('img', file_name),image)
        aws_service.get_image_for_search(file_name)
        stop_camera()
    else :
        detection_face()

def stop_camera() :
    camera.stop_preview()
        
def start_camera() :
    camera.resolution = (640, 480)
    camera.start_preview(fullscreen=False, window=(100,100,400,400))
    detection_face()

if __name__ == "__main__":
    start_camera()
    while True :
        try:
            command = str(raw_input('command : '))
            if command == 'stop' :
                print('Stop Camera')
                stop_camera()
            elif command == 'start' :
                print('Start Camera')
                start_camera()
        except ValueError:
            print ('Not a string')
