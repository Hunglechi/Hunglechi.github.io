import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3
from datetime import datetime
import os

"""This file is used to check the accuracy by running 
read data from "'trainningData.yml'" to predict the ID of the image
in the file "dataTest". Percent correct is the total number of correctly guessed pictures
divided by the number of predicted pictures"""


#use CV2 in Opencv library
faceDetect = cv2.CascadeClassifier(
    'C:\\Users\\Hung\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
rec = cv2.face.LBPHFaceRecognizer_create()

#Read file 'trainningData.yml' to detect face
rec.read('trainningData.yml')
path = 'dataTest'
imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
number_true = 0
total = 0
for test_image in imagePaths:
    total = total + 1
    image = Image.open(test_image).convert('L')
    image_np = np.array(image, 'uint8')

    # Before giving the image to the model lets check it first
    predictions = rec.predict(image_np)
    print(predictions)
    expected_output = int(os.path.split(test_image)[1].split(' ')[0].replace("subject", " "))
    print(expected_output)
    if (predictions[0] == expected_output):
        number_true = number_true + 1

print("number true: ", number_true)
print("total:", total)
print("Phan tram: ", number_true / total * 100)
