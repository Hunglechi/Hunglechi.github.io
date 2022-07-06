import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3
from datetime import datetime
import os

"""This is the same file as the detector file, 
but the system will ask to take a picture of the face, 
then the system will predict the name and ID of the face."""

def getProfile(id):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE PID=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


faceDetect = cv2.CascadeClassifier(
    'C:\\Users\\Hung\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
rec = cv2.face.LBPHFaceRecognizer_create();
rec.read('trainningData.yml')

# Establish a connection to the webcam
cam = cv2.VideoCapture(0)
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        'C:\\Users\\Hung\\anaconda3\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('frame', img)
    # wait for 100 miliseconds
    if cv2.waitKey(100) & 0xFF == ord('c'):
        cv2.imwrite("cameraCheck/" + 'input_image.jpg', gray[y:y + h, x:x + w])
        break
cam.release()
cv2.destroyAllWindows()

path = 'cameraCheck'
imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
for test_image in imagePaths:
    image = Image.open(test_image).convert('L')
    image_np = np.array(image, 'uint8')

    # Before giving the image to the model lets check it first
    cv2.imshow('frame', image_np)
    predictions = rec.predict(image_np)
    profile = getProfile(predictions[0])
    if (profile!=None):
        print("ID: " + str(profile[0]))
        print("Name: " + str(profile[1]))
    else:
        print("Unknow")