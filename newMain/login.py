import os
import time
from cvzone.HandTrackingModule import HandDetector
import Finger
import Tag
import VirtualKeyboard
import numpy as np
import cv2
import serial
import AttendanceProject
import hangul

def login(winTitle, cap):

    # ID/PW 리스트
    idPwList = [("202217001", "노영주", "I", "5"), ("202127007", "이지은", "J", "6"), ("202217015", "서재형", "s", "1"),
                ("202217018", "최유이", "C", "18"), ("202217008", "김수영", "K", "8")]
    imgBackground = cv2.imread("Resources/Background_test1.png")

    # 화면 글씨 출력 폰트 객체 생성
    #fontpath = "NanumGothic.ttc"
    #font64 = ImageFont.truetype(fontpath, 64)

    # importing all the mode images to a list (우측 화면 그림 등록)
    folderPathModes = "Resources/Modes"
    listImgModesPath = os.listdir(folderPathModes)
    listImgModes = []
    for imgModePath in listImgModesPath:
        listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))
    print(listImgModes)

    # importing all the icons to a list (좌측 하단 아이콘 그림 등록)
    folderPathIcons = "Resources/Icons"
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

    errMsg = ""

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 좌우반전(10/30)
        # Find the hand and its landmarks
        hands, img = detector.findHands(img, flipType=False)  # with draw
        # overlaying the webcam feed on the background image
        # 카메라 영상(1280x720) 영상 크기를 853x480으로 조정한후, 가운데 영역만 잘라 640x480으로 생성 (10/30)
        imgBackground[139:139 + 480, 50:50 + 640] = cv2.resize(img, (853, 480))[0:480, 56:696]
        imgBackground[0:720, 847: 1280] = listImgModes[0]

        if hands and counterPause == 0 and modeType < 4:  # <3이었음
            # Hand 1
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)
            print(fingers1)

            if fingers1[1:] == [1, 0, 0, 0]:
                if selection != 1:
                    counter = 1
                selection = 1
            elif fingers1[1:] == [1, 1, 0, 0]:
                if selection != 2:
                    counter = 1
                selection = 2
            elif fingers1[1:] == [1, 1, 1, 0]:
                if selection != 3:
                    counter = 1
                selection = 3
            elif fingers1[1:] == [1, 1, 1, 1]:
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
                    #modeType += 1
                    counter = 0
                    selection = -1
                    counterPause = 1

        # To pause after each selection is made
        if counterPause > 0:
            counterPause += 1
            if counterPause > 60:
                counterPause = 0

        # Add selection icon at the bottom
        if selectionList[0] == 1:
            #imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
            inId = VirtualKeyboard.readKeyboard(winTitle, cap, "아이디를 입력하세요.")
            inPw = VirtualKeyboard.readKeyboard(winTitle, cap, "패스워드를 입력하세요.")
            #inId = "I" # 테스트용
            #inPw = "6" # 테스트용
            print(inId, inPw)
            for hakbun, name, id, pw in idPwList:
                if id==inId and pw==inPw:
                    print(hakbun, name)
                    return hakbun, name
            selectionList[0] = -1

            # ID/PW 오류메시지 출력
            errMsg = "아이디 또는 패스워드가 틀렸습니다."
            imgBackground = cv2.imread("Resources/Background_test1.png")

        # 얼굴 인식
        if selectionList[0] == 2:
            #imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
            #imgBackground[0:720, 847: 1280] = listImgModes[1]
            hakbun, name = AttendanceProject.recognizeFace(winTitle, cap)
            #얼굴인식 오류 메세지 출력
            if hakbun == "none":
                errMsg = "등록된 얼굴이 아닙니다.        "
            else:
                return hakbun, name
            selectionList[0] = -1
            imgBackground = cv2.imread("Resources/Background_test1.png")

        if selectionList[0] == 3:
            #imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]
            imgBackground[0:720, 847: 1280] = listImgModes[2]
            hakbun, name = Finger.fingerprint() #지문인식
            if hakbun == "none":
                errMsg = "등록된 지문이 아닙니다.        "
            else:
                return hakbun, name
            selectionList[0] = -1
            imgBackground = cv2.imread("Resources/Background_test1.png")

        if selectionList[0] == 4:
            #imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[3]]
            imgBackground[0:720, 847: 1280] = listImgModes[3]
            hakbun, name = Tag.readTag()  # 태그인식
            if hakbun == "none":
                errMsg = "등록된 학생증이 아닙니다.       "
            else:
                return hakbun, name
            selectionList[0] = -1
            imgBackground = cv2.imread("Resources/Background_test1.png")

        #글자 위치 !!!!!!!!!
        if len(errMsg):
            imgBackground = hangul.putHgText(imgBackground, errMsg, (120, 648), hangul.font[25], hangul.RED)


        # Displaying
        # cv2.imshow("Image", img)
        cv2.imshow(winTitle, imgBackground)  # 이름 붙인 윈도우에 출력하기 (10/30)
        cv2.waitKey(1)


if __name__ == "__main__":
    # 카메라 설정. 노트북은 0으로 할 것
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # 해상도 변경(10/30)
    cap.set(4, 720)  # 해상도 변경(10/30)
    login("login", cap)
