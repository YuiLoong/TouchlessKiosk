import sys
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
from PIL import ImageFont, ImageDraw, Image
import VirtualMouse
import selectCertificate
import login
import hangul



# 한글 출력 설정
fontpath = "NanumGothic.ttc"
font = []
for i in range(6, 129):
    font.append(ImageFont.truetype(fontpath, i))  # 6부터 128까지 크기의 폰트 준비

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


def putHgText(frame, text, loc, font, color=(255, 255, 255)):
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text(loc, text, font=font, fill=color)
    return np.array(img_pil)

#while문 전체 쏘기

def printCertificate(title, cap, hakbun, name, number):

    imgBackground = cv2.imread("Resources/Background_test1.png")
    detector = HandDetector(detectionCon=0.8)
    btn = VirtualMouse.Button((500, 500), "확인", [150, 100])

    while True:
        success, img = cap.read()
        if success == False:
            continue
        img = cv2.flip(img, 1)  # 좌우반전(10/30)
        # Find the hand and its landmarks
        hands, img = detector.findHands(img)  # with draw
        # overlaying the webcam feed on the background image
        # 카메라 영상(1280x720) 영상 크기를 853x480으로 조정한후, 가운데 영역만 잘라 640x480으로 생성 (10/30)

        # 확인 버튼 생성
        img, bbox = cvzone.putTextRect(img, "OK", [500, 500], 10, 2, offset=30, border=0)
        btn = VirtualMouse.Button((bbox[0], bbox[1]), "확인", (bbox[2] - bbox[0], bbox[3] - bbox[1]))
        print(bbox)

        if hands:
            lmList = hands[0]["lmList"]  # hands로부터 lmList 획득
        else:  # hands가 검출이 안되었으면 lmList는 빈 걸로
            lmList = []

        if lmList:
            hx, hy, hw, hh = hands[0]['bbox']  # 손 박스 위치, 크기

            handCenterX = hx + hw // 2  # 손 중심 X 좌표
            handCenterY = hy + hh // 2  # 손 중심 Y 좌표

            # cv2.rectangle()
            cv2.circle(img, (handCenterX, handCenterY), 10, (0, 255, 0), -1)  # 손 중심에 원 그리기
            if VirtualMouse.fingerRightClick(detector, hands[0]):
                if VirtualMouse.press((handCenterX, handCenterY), btn):
                    return

        imgBackground[139:139 + 480, 50:50 + 640] = cv2.resize(img, (853, 480))[0:480, 56:696]


        if number == 1:
            imgBackground[0:720, 847: 1280] = cv2.imread("PrintResource/print1.png")
            imgBackground = putHgText(imgBackground, hakbun,  (920,400), font[50],(0,0,0))
            imgBackground = putHgText(imgBackground, name,  (1000,330), font[50],(0,0,0))



        if number == 2:
            imgBackground[0:720, 847: 1280] = cv2.imread("PrintResource/print2.png")
            imgBackground = putHgText(imgBackground, hakbun,  (920,400), font[50],(0,0,0))
            imgBackground = putHgText(imgBackground, name,  (1000,330), font[50],(0,0,0))

        if number == 3:
            imgBackground[0:720, 847: 1280] = cv2.imread("PrintResource/print3.png")
            imgBackground = putHgText(imgBackground, hakbun,  (920,400), font[50],(0,0,0))
            imgBackground = putHgText(imgBackground, name,  (1000,330), font[50],(0,0,0))

        if number == 4:
            imgBackground[0:720, 847: 1280] = cv2.imread("PrintResource/print4.png")
            imgBackground = putHgText(imgBackground, hakbun,  (920,400), font[50],(0,0,0))
            imgBackground = putHgText(imgBackground, name,  (1000,330), font[50],(0,0,0))



        cv2.imshow(title, imgBackground)
        cv2.waitKey(1)

if __name__ == "__main__":
    # 카메라 설정. 노트북은 0으로 할 것
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # 해상도 변경(10/30)
    cap.set(4, 720)  # 해상도 변경(10/30)
    #테스트
    printCertificate("printCertificate", cap, "202217015","서재형",1)