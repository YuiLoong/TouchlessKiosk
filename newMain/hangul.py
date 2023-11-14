from PIL import ImageFont, ImageDraw, Image
import numpy as np

# 한글 출력 설정
fontpath = "NanumGothic.ttc"
font = []
for i in range(6, 129):
    font.append(ImageFont.truetype(fontpath, i))  # 6부터 128까지 크기의 폰트 준비

# 컬러
WHITE = (255, 255, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)
BLACK = (0, 0, 0)
def putHgText(frame, text, loc, font, color=(255, 255, 255)):
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text(loc, text, font=font, fill=color)
    return np.array(img_pil)