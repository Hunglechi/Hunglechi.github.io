import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3
from datetime import datetime

"""this is the file used to detect faces in real time for attendance. 
The face will be displayed with the name and ID. If the face does not exist,
 "Unknown" will appear on the screen. When the name and ID information is correct, 
 we can press the "c" key to take attendance in the file Diemdanh.csv. """

#use CV2 in Opencv library
faceDetect = cv2.CascadeClassifier('C:\\Users\\Hung\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()

#Read file 'trainningData.yml' to detect face
rec.read('trainningData.yml')
id = 0

# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203, 23, 252)

# Write attendance name in 'Diemdanh.csv'
def Attendance(name, valmin):
    with open('Diemdanh.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        # if name not in nameList:
        now = datetime.now()
        dtString = now.strftime('%d/%m/%Y, %H:%M:%S')
        f.writelines(f'\n{name},{dtString},{valmin}')

# get data from sqlite by ID
def getProfile(id):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE PID=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


while (True):
    # camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        id, conf = rec.predict(gray[y:y + h, x:x + w])
        print(conf)
        profile = getProfile(id)

        # set text to window
        #When profile has data and conf lower 70, we put infor to screen
        # conf is confidence parameter, The smaller the "conf", the greater the accuracy rate
        if (profile != None and conf <70):
            cv2.putText(img, "ID: " + str(profile[0]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)

        #if profile do not have data and conf bigger 70, we put "Unknow" to screen
        else:
            cv2.putText(img, "Unknow", (x + 10, y + 10), fontface, 1, (0, 0, 255), 2)
        cv2.imshow('Face', img)

    #Press "c" key to write attendance name in 'Diemdanh.csv'
    if cv2.waitKey(1) == ord('c'):
        Attendance(profile[0], profile[1])
        print("Checked")

    # Quit when we press key "q"
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
