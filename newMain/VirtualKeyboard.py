import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import hangul

detector = HandDetector(detectionCon=0.8)

keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

Smkeys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
          ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
          ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
          ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]]

Spkeys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
          ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"],
          ["`", "~", "-", "_", "=", "+", "/", "?", "{", "}"],
          ["\\","|", ";", ":", "\'",'\"',"<", ">", ",", "."]]

Skeys = [["<-"],
        ["Aa"],
         ["!@"]]

Sendkey = [["SEND"]]

keyboard = Controller()

prevLeftPressed = False
leftPressed = False
prevRightPressed = False
rightPressed = False

def fingerLeftClick(hand):
    fingers = detector.fingersUp(hand)[1:]  # 엄지는 제외하고 복사
    #print(fingers)
    uCnt = sum(fingers)
    #print(uCnt)
    global leftPressed, prevLeftPressed

    if uCnt == 4:
        leftPressed = False
    elif uCnt == 0 and leftPressed== False:
        leftPressed = True

    leftClick = True if  leftPressed == True and prevLeftPressed == False else False
    prevLeftPressed = leftPressed

    return leftClick

def fingerRightClick(hand):
    fingers = detector.fingersUp(hand)[1:]  # 엄지는 제외하고 복사
    #print(fingers)
    uCnt = sum(fingers)
    #print(uCnt)
    global rightPressed, prevRightPressed

    if uCnt == 4:
        rightPressed = False
    elif uCnt == 0 and rightPressed== False:
        rightPressed = True

    rightClick = True if rightPressed == True and prevRightPressed == False else False
    prevRightPressed = rightPressed

    return rightClick

def press(handRect, keyRect):
    cx, cy = handRect
    x, y = keyRect.pos
    w, h = keyRect.size

    if cx > x and cx < x + w and cy > y and cy < y + h:
        return True
    return False

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

def drawSend(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 45, y + 70),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

def readKeyboard(winTitle, cap, msg):
    finalText = ""
    toggle = False
    buttonList = []
    SbuttonList = []
    TbuttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i + 150], key))

    for i in range(len(Skeys)):
        for j, key in enumerate(Skeys[i]):
            SbuttonList.append(Button([100 * j + 1050, 100 * i + 150], key, [150, 85]))

    for i in range(len(Sendkey)):
        for j, key in enumerate(Sendkey[i]):
            TbuttonList.append(Button([100 * j + 750, 100 * i + 550], key, [250, 100]))

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)          # 좌우 뒤집기 (23/06/09)
        hands, img = detector.findHands(img, flipType=False)        # hands 추가 (23/06/09)
        if hands:
            lmList = hands[0]["lmList"]                 # hands로부터 lmList 획득 (23/06/09)
            #lmList, bboxInfo = detector.findPosition(img)  # cvzone v1.5.6 패키지에는 findPosition이 없음
        else:                                   # hands가 검출이 안되었으면 lmList는 빈 걸로
            lmList = []

        img = hangul.putHgText(img, msg, (50,50), hangul.font[64], hangul.YELLOW)
        img = drawAll(img, buttonList)
        img = drawAll(img, SbuttonList)
        img = drawSend(img, TbuttonList)

        if lmList:
            hx, hy, hw, hh = hands[0]['bbox']   # 손 박스 위치, 크기

            handCenterX = hx + hw // 2          # 손 중심 X 좌표
            handCenterY = hy + hh // 2          # 손 중심 Y 좌표

            cv2.circle(img,(handCenterX, handCenterY), 10,(0, 255, 0), -1)  # 손 중심에 원 그리기
            if fingerRightClick(hands[0]):
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    if press((handCenterX, handCenterY), button):
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.5)     # 0.15초 대신 0.5초로 변경 (23/06/09)'''

                for button in SbuttonList:
                    x, y = button.pos
                    w, h = button.size

                    if press((handCenterX, handCenterY), button):
                        if press((handCenterX, handCenterY), SbuttonList[0]):
                            if len(finalText) > 0:
                                finalText = finalText[:len(finalText)-1]  # Remove the last character
                        elif press((handCenterX, handCenterY), SbuttonList[1]):
                            buttonList = []
                            if toggle == False:
                                for i in range(len(Smkeys)):
                                    for j, key in enumerate(Smkeys[i]):
                                        buttonList.append(Button([100 * j + 50, 100 * i + 150], key))
                                toggle = True
                            else:
                                for i in range(len(keys)):
                                    for j, key in enumerate(keys[i]):
                                        buttonList.append(Button([100 * j + 50, 100 * i + 150], key))
                                toggle = False

                        elif press((handCenterX, handCenterY), SbuttonList[2]):
                            buttonList = []
                            for i in range(len(Spkeys)):
                                for j, key in enumerate(Spkeys[i]):
                                    buttonList.append(Button([100 * j + 50, 100 * i + 150], key))

                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        #finalText += button.text
                        sleep(0.5)     # 0.15초 대신 0.5초로 변경 (23/06/09)'''

                for button in TbuttonList:
                    x, y = button.pos
                    w, h = button.size
                    if press((handCenterX, handCenterY), button):
                        print(finalText)
                        return finalText

        cv2.rectangle(img, (50, 550), (700, 650), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 630),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cv2.imshow(winTitle, img)
        k = cv2.waitKey(1)          # 키입력을 1ms 동안 기다림, k 추가(23/06/09)
        if k == ord('q'):           # q를 누르면 프로그램 종료 추가 (23/06/09)
            return

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    readKeyboard("VirtualKeyboard", cap, "아이디를 입력하세요.")