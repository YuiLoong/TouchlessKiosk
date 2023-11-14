from cvzone.HandTrackingModule import HandDetector

prevLeftPressed = False
leftPressed = False
prevRightPressed = False
rightPressed = False

#detector = HandDetector(detectionCon=0.8)

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

def fingerLeftClick(detector, hand):
    fingers = detector.fingersUp(hand)[1:]  # 엄지는 제외하고 복사
    #print(fingers)
    uCnt = sum(fingers)
    #print(uCnt)
    global leftPressed, prevLeftPressed
    if uCnt == 4:
        leftPressed = False
    elif uCnt == 0 and leftPressed== False:
        leftPressed = True
    # if leftPressed == True and prevLeftPressed == False:
    #     leftClick = True
    # else:
    #     leftClick = False
    leftClick = True if  leftPressed == True and prevLeftPressed == False else False
    prevLeftPressed = leftPressed

    return leftClick

def fingerRightClick(detector, hand):
    fingers = detector.fingersUp(hand)[1:]  # 엄지는 제외하고 복사
    #print(fingers)
    uCnt = sum(fingers)
    #print(uCnt)
    global rightPressed, prevRightPressed
    if uCnt == 4:
        rightPressed = False
    elif uCnt == 0 and rightPressed== False:
        rightPressed = True
    # if rightPressed == True and prevRightPressed == False:
    #     rightClick = True
    # else:
    #     rightClick = False
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
