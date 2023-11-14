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
import printCertificate

# 한글 출력 설정
fontpath = "NanumGothic.ttc"
font = []
for i in range(6, 129):
    font.append(ImageFont.truetype(fontpath, i))  # 6부터 128까지 크기의 폰트 준비

def putHgText(frame, text, loc, font, color=(255, 255, 255)):
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text(loc, text, font=font, fill=color)
    return np.array(img_pil)

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

def introScreen(title, cap):

    detector = HandDetector(detectionCon=0.8)
    btn = VirtualMouse.Button((500, 500), "Login", [150, 100])

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 좌우반전(10/30)
        # Find the hand and its landmarks
        hands, img = detector.findHands(img, draw=False, flipType=False)  # with draw

        # 타이틀
        img = putHgText(img, "Toucheless Kiosk", (350, 200), font[64],(0, 255,2255))
        img = putHgText(img, "학적증명서 발급 시스템", (300, 300), font[64], (255,255,255))
        img = putHgText(img, "AI소프트웨어과 ACE동아리", (320, 550), font[50], (210, 150, 55))



        # 로그인 버튼 생성
        img, bbox = cvzone.putTextRect(img, "Login", [600, 450], 2, 2, offset=30, border=0)
        btn = VirtualMouse.Button((bbox[0], bbox[1]), "login", (bbox[2]-bbox[0], bbox[3]-bbox[1]))
        print(bbox)

        if hands:
            lmList = hands[0]["lmList"]  # hands로부터 lmList 획득
        else:  # hands가 검출이 안되었으면 lmList는 빈 걸로
            lmList = []

        if lmList:
            hx, hy, hw, hh = hands[0]['bbox']  # 손 박스 위치, 크기

            handCenterX = hx + hw // 2  # 손 중심 X 좌표
            handCenterY = hy + hh // 2  # 손 중심 Y 좌표

            #cv2.rectangle()
            cv2.circle(img, (handCenterX, handCenterY), 10, (0, 255, 0), -1)  # 손 중심에 원 그리기
            if VirtualMouse.fingerRightClick(detector, hands[0]):
                if VirtualMouse.press((handCenterX, handCenterY), btn):
                    return

        cv2.imshow(title, img)
        cv2.waitKey(1)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

title = "Touchless Kiosk"

while True:
    introScreen(title, cap)
    hakbun, name = login.login(title, cap)
    number = selectCertificate.selectCertificate(title, cap)
    printCertificate.printCertificate(title, cap, hakbun, name, number)

