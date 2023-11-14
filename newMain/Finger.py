import time

import serial

students =[["202317005","이가현","2"],
           ["202317004","고영휘","3"]]

# 포트와 보드레이트로 초기화된 serial 객체를 생성한다.
pyserial = serial.Serial(port='COM3', baudrate=9600)

def fingerprint():
    while True:
        stime = time.time()
        if pyserial.readable():
            # 시리얼 통신 버퍼로부터 한개 라인을 읽어들인다.
            response = pyserial.readline()
            # 바이트열 끝에 있는 '\n\r'을 제외하고 문자열로 변환해 출력한다.
            response = response[:len(response)-2].decode()
            print(response)

            for num in students:
                if num[2]==response:
                    print(num[0],num[1])
                    return  num[0],num[1]

            print("none")
            return "none","none"
        etime = time.time()
        if etime - stime > 10:
            return "none","none"
if __name__ == "__main__":
    while True:
        fingerprint()