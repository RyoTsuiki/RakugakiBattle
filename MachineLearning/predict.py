import np_load
import numpy as np
from tensorflow.python.keras.models import load_model
import cv2
import sys

FILE_PATH = "/home/labmember/Desktop/teamb/standard/class_345/result.csv"

def find_squares_gray(img):
    """
    グレースケール画像から余白を切り取る関数
    img : グレースケール画像 ndarray
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
    '''
    ある特定のRGB値の部分を切り取る関数
    img : 切り取る前のカラー画像 ndarray
    b : 青の
    '''
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
    """
    スクリーンショットされた画像の切り取り
    img_path : 画像のパス
    return : 加工した画像 ndarray
    """
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
    #cv2.imwrite("22.jpg", result)predict_proba
    # グレースケール変換
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    print("convert gray")
    # 余白を切り抜く
    left, right, top, botom = find_squares_gray(result)
    result = clipping_img(result, left, right, top, botom)
    print("cut margin")
    print(left, right, top, botom)
    return result

def predict(model, img_path, label_path, prepro_flag = False, raw_model_flag = False, save_flag = False, odai = None):
    """
    推論した結果を辞書型に格納して返す関数
    model : 使用するモデルのパス
    img_path : 推論させる画像のパス
    label_path : 使用するラベルのパス
                 ラベル:クラス名とそれに対応する数を格納したcsvファイル
    prepro_flag : 画像を切り抜き処理するかを指定するフラグ
                  True:切り抜きを行う, False:切り抜きを行わない(デフォルト値)
    raw_model_flag : True:モデルを直接読み込む Author:RyoTsuiki
    """
    # 画像をカラー画像で読み込み切り抜きを行う
    if prepro_flag: img = preprocessing(img_path)
    # 画像をグレースケールで読み込む
    else: img = cv2.imread(img_path,0)
    #例外処理
    if(img is None):
        return None
    # 輝度値変換
    img = 255 - img
    # 画像の正規化
    img = img / 255.
    # 画像のリサイズ(縦横比を保ち長い方を28に)
    org_lens = np.shape(img)
    if(org_lens[0] < org_lens[1]):
        img = cv2.resize(img, (28, min(org_lens[0]*28//org_lens[1]+1,28)))
    else:
        img = cv2.resize(img, (min(org_lens[1]*28//org_lens[0]+1,28), 28))
    #28*28の背景にリサイズした画像を貼り付け
    imgback = np.zeros((28, 28), np.uint8)
    aft_lens = np.shape(img)
    sy = (28-aft_lens[0])//2
    sx = (28-aft_lens[1])//2
    for i in range(aft_lens[0]):
        for j in range(aft_lens[1]):
            imgback[i+sy][j+sx] += img[i][j]
    img = imgback
    #print(img.shape)
    # モデルの読み込み
    if(not raw_model_flag):model = load_model(model)
    # 推論させる
    proba = model.predict_proba(img.reshape(1, 28, 28, 1))


    #print(proba)
    # ラベルのキーと値を反転させる
    label = {v: k for k, v in np_load.get_label(label_path).items()}
    # 推論結果をクラス名とその値をセットにした辞書型にする {class:score}
    score = {classes: score for classes, score in zip(label.values(), proba[0])}
    if save_flag:
        data = odai + ","
        for value in score.values():
            data += str(value) + ","
        data += img_path
        data += "\n"
        with open(FILE_PATH,mode = "a") as f:
            f.write(data)
    # score をもとに降順に並び替える
    score_sorted = sorted(score.items(), key=lambda x:x[1], reverse=True)
    # list -> dict
    score_sorted = {classes: score for classes, score in score_sorted}
    #読み込んだ画像表示
    for i in range(28):
        s = ""
        for j in range(28):
            if(img[i][j] > 0.5):s += "黒"
            elif(img[i][j] > 0):s += "灰"
            else:s+= "　"
        print(s)
    return score_sorted

if __name__ == "__main__":
    args = sys.argv[1:]
    print(predict(args[0], args[1], args[2], True))
    #print(predict("test.h5", "dog.jpg", label.csv))
