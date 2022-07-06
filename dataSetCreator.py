import cv2
import sqlite3

"""This is the file used to create a new user's data set into
  the facial recognition system for attendance. Users will 
  take around 100 photos of their own face along with their name and ID. 
  Then the information will be saved to the Database and the face will be trained
  in the recognition system."""

cam = cv2.VideoCapture(0)
# insert/update data to sqlite
def insertOrUpdate(id, name):
    conn = sqlite3.connect("FaceBase.db")
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS People')

    cur.execute('''
    CREATE TABLE People (PID TEXT, PName TEXT)''')

    cur.execute('SELECT PName FROM People WHERE PID = ? ', (str(id),))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO People (PID, PName) VALUES (?, ?)''', (str(id), str(name)))
    else:
        cur.execute('UPDATE People SET PID = ? WHERE PName = ?', (str(id), str(name)))
    conn.commit()
    conn.close()

#Input information student
id = input('Enter your ID: ')
name = input('Enter your Name: ')
#Save information into DataBase
insertOrUpdate(id, name)

#Use CV2 to read face
sampleNum = 0
while (True):
    # camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        'C:\\Users\\Hung\\anaconda3\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # incrementing sample number
        sampleNum = sampleNum + 1

        # saving the captured face in the dataset folder
        cv2.imwrite("dataTraining/" + str(str(id)+' '+str(name)) + ' ' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

        #show the frame
        cv2.imshow('frame', img)

    # wait for 100 miliseconds to take picture
    #Quit when we press key "q"
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    # break if the sample number is more than 101
    elif sampleNum > 101:
        break
cam.release()
cv2.destroyAllWindows()
