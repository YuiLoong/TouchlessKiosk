import serial

students = [["202317004", "고영휘", " 65 AD 82 B0"],
            ["202317008", "홍길동", " 62 D7 ED 51"],
            ["202217007", "이지은", " D1 AD E4 7C"]]

pyserial = serial.Serial(port='COM6', baudrate=9600)

def readTag():
    while True:
        if pyserial.readable():
            # 시리얼 통신 버퍼로부터 한개 라인을 읽어들인다.
            response = pyserial.readline()
            # 바이트열 끝에 있는 '\n\r'을 제외하고 문자열로 변환해 출력한다.
            response = response[:len(response)-2].decode()
            print(response)
            for num in students:
                if num[2] == response:
                    print(num[0],num[1])
                    return num[0], num[1]
            print("none")
            return "none", "none"

if __name__ == "__main__":
    while True:
        readTag()