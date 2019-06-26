import np_load
import numpy as np
from tensorflow.python.keras.models import load_model
import cv2
import sys


def find_squares_gray(img):
    """
    グレースケール画像から余白を切り取る関数
    img : グレースケール画像
    return : left, right, top, botom
    """
    x = []
    y = []
    for idy, line in enumerate(img):
        for idx, value in enumerate(line):
            if not value == 255:
                x.append(idx)
                y.append(idy)
    return (min(x), max(x), min(y), max(y))


def find_squares_color(img, b, g, r):
    left = right = top = botom = 0
    x = []
    y = []
    for idy, line in enumerate(img):
        for idx, value in enumerate(line):
            if (value[0] == b) and (value[1] == g) and (value[2] == r):
                x.append(idx)
                y.append(idy)
    if not x:
        left = 0
        right = img.shape[1]
    else:
        left = min(x)
        right = max(x)

    if not y:
        top = 0
        botom = img.shape[0]
    else:
        top = min(y)
        botom = max(y)
    return (left, right, top, botom)


def clipping_img(img, left, right, top, botom):
    """
    入力されたグレースケール画像を指定した位置で短形に切り取る関数
    img : グレースケール画像
    left : 切り取る位置の左端
    righty : 切り取る位置の右端
    top : 切り取る位置の上端
    botom : 切り取る位置の下端
    return : 切り取った画像
    """
    return img[top:botom, left:right]


def preprocessing(img_path):
    # 画像の読み込み
    img = cv2.imread(img_path)
    # オレンジ色部分で切り出し
    # いきなり白で切り抜くと上部がヘッダの電波マークになるため
    left, right, top, botom = find_squares_color(img, 52, 183, 250)
    # なぜか上手くいかなかったため, 直打ち
    result = clipping_img(img, 0, img.shape[0], top, botom)
    print("cut orange")
    print(left, right, top, botom)
    #cv2.imwrite("21.jpg", result)
    # 白で切り出し
    left, right, top, botom = find_squares_color(result, 255, 255, 255)
    result = clipping_img(result, left, right, top, botom)
    print(left, right, top, botom)
    print("cut white")
    #cv2.imwrite("22.jpg", result)
    # グレースケール変換
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    print("convert gray")
    # 余白を切り抜く
    left, right, top, botom = find_squares_gray(result)
    result = clipping_img(result, left, right, top, botom)
    print("cut margin")
    print(left, right, top, botom)
    return result

def predict(model, img_path, prepro_flag = False):
    if prepro_flag: img = preprocessing(img_path)
    else: img = cv2.imread(img_path,0)
    img = cv2.resize(img, (28, 28))
    print(img.shape)
    model = load_model(model)
    proba = model.predict_proba(img.reshape(1, 28, 28, 1))
    label = {v: k for k, v in np_load.LABEL.items()}
    return {classes: score for classes, score in zip(label.values(), proba[0])}

if __name__ == "__main__":
    args = sys.argv[1:]
    print(predict(args[0], args[1], True))
    #print(predict("test.h5", "dog.jpg"))