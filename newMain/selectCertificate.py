import os
import time
from cvzone.HandTrackingModule import HandDetector
import VirtualKeyboard
import numpy as np
import cv2
import AttendanceProject
import hangul

def selectCertificate(title, cap):


    imgBackground = cv2.imread("Resources/Background_test1.png")


    # importing all the mode images to a list (우측 화면 그림 등록)
    folderPathMode = "SelectResource/Mode1"
    listImgModesPath = os.listdir(folderPathMode)
    listImgMode = []
    for imgModePath in listImgModesPath:
        listImgMode.append(cv2.imread(os.path.join(folderPathMode, imgModePath)))
    print(listImgMode)

    # importing all the icons to a list (좌측 하단 아이콘 그림 등록)
    folderPathIcons = "SelectResource/Icons"
    listImgIconsPath = os.listdir(folderPathIcons)
    listImgIcons = []
    for imgIconsPath in listImgIconsPath:
        listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))

    # 글로벌 변수 초기화
    modeType = 0  # for changing selection mode
    selection = -1
    counter = 0
    selectionSpeed = 14
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    modePositions = [(1155, 180), (977, 323), (1165, 463), (980, 602)]  # 여기 고치기 (가로,세로)= (왼->오,위->아래)방향
    counterPause = 0
    selectionList = [-1, -1, -1, -1]  # 1~4고르기 전 베이스
    number = 0 #출력 시 if문에 쓰일

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 좌우반전(10/30)
        # Find the hand and its landmarks
        hands, img = detector.findHands(img)  # with draw
        # overlaying the webcam feed on the background image
        # 카메라 영상(1280x720) 영상 크기를 853x480으로 조정한후, 가운데 영역만 잘라 640x480으로 생성 (10/30)
        imgBackground[139:139 + 480, 50:50 + 640] = cv2.resize(img, (853, 480))[0:480, 56:696]
        imgBackground[0:720, 847: 1280] = listImgMode[0]

        if hands and counterPause == 0 and modeType < 4:  # <3이었음
            # Hand 1
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)
            #print(fingers1)

            if fingers1 == [0, 1, 0, 0, 0]:
                if selection != 1:
                    counter = 1
                selection = 1
            elif fingers1 == [0, 1, 1, 0, 0]:
                if selection != 2:
                    counter = 1
                selection = 2
            elif fingers1 == [0, 1, 1, 1, 0]:
                if selection != 3:
                    counter = 1
                selection = 3
            elif fingers1 == [0, 1, 1, 1, 1]:
                if selection != 4:
                    counter = 1
                selection = 4
            else:
                selection = -1
                counter = 0

            if counter > 0:
                counter += 1
                #print(counter)

                cv2.ellipse(imgBackground, modePositions[selection - 1], (80, 80), 0, 0,  # 원 사이즈
                            counter * selectionSpeed, (0, 255, 0), 20)
                if counter * selectionSpeed > 360:
                    selectionList[modeType] = selection
                    print("selection list = ", end=" ")
                    print(selectionList)
                    modeType += 1
                    counter = 0
                    selection = -1
                    counterPause = 1

        # To pause after each selection is made
        if counterPause > 0:
            counterPause += 1
            if counterPause > 60:
                counterPause = 0

        # 고를 시 밑 아이콘
        # 1번 고를 시
        if selectionList[0] == 1:
            #imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
            selectionList[0] = -1
            number = 1
            return number #증명서 종류
        # 2번 고를 시
        if selectionList[0] == 2:
            #imgBackground[636:636 + 65, 133:133+ 65] = listImgIcons[2 + selectionList[1]] #[636:636 + 65, 340:340 + 65]
            #hakbun, name = AttendanceProject.recognizeFace(winTitle, cap)
            #print(hakbun, name)
            #return hakbun, name
            selectionList[0] = -1
            number = 2
            return number
        # 3번 고를 시
        if selectionList[0] == 3:
            #imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[2]-1]
            selectionList[0] = -1
            number = 3
            return number
        # 4번 고를 시
        if selectionList[0] == 4:
            #imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[3]]
            selectionList[0] = -1
            number = 4
            return number
        # Displaying
        # cv2.imshow("Image", img)
        cv2.imshow(title, imgBackground)  # 이름 붙인 윈도우에 출력하기 (10/30)
        cv2.waitKey(1)




if __name__ == "__main__":
    # 카메라 설정. 노트북은 0으로 할 것
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)  # 해상도 변경(10/30)
    cap.set(4, 720)  # 해상도 변경(10/30)
    selectCertificate("selectCertificate", cap)