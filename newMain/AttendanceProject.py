import time

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
#from PIL import ImageGrab
import hangul

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

def findEncodings(images):
    encodeList = []
    print(len(images))
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'n{name},{dtString}')

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

def recognizeFace(winTitle, cap):
    studentList = [("202217001", "노영주"),("202217007", "이지은"), ("202217015", "서재형"),
                   ("202217018", "최유이")]

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    count = 0
    prevName = ""

    stime = time.time()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25, cv2.INTER_LINEAR)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        img = hangul.putHgText(img, "얼굴 인식", (500, 50), hangul.font[64], hangul.YELLOW)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)

            if faceDis[matchIndex]< 0.4:
                name = classNames[matchIndex].upper()
                if name == prevName:
                    count = count + 1
                else:
                    count = 0
            else:
                name = 'Unknown'
                count = 0
            print(name, count)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
            if count == 10:
                markAttendance(name)
                for snum, sname in studentList:
                    if snum == name:
                        print(snum, sname)
                        time.sleep(3)
                        return snum, sname
            prevName = name

        cv2.imshow(winTitle,img)
        cv2.waitKey(1)

        etime = time.time()
        print(etime-stime)
        if etime - stime > 7:
            return "none", "none"

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    recognizeFace("Face Recognition", cap)