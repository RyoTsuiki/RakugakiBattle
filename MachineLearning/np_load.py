import numpy as np
import math
import glob
import csv

#FILE_PATH = "/home/share/data/"
FILE_PATH = "../data/"
#FILE_PATH = ""

X_DATA_SHAPE = (0, 28, 28, 1)
Y_DATA_SHAPE = (0,)
EXTENSION = ".npy"
LABEL = None

def __create_label():
    '''
    クラス名とそれに対応した値(辞書型)を返す
    keys: class name (English)
    values: 0-len(keys) 読み込んだ順につける
    クラス名はフォルダー内の".npy"ファイルから取得
    戻り値: クラス名とそれに対応した値 (辞書型)
    '''
    keys = __search_files()
    values = range(len(keys))
    global LABEL
    LABEL = dict(zip(keys, values))
    return LABEL

def get_data_shape():
    '''
    学習/テストデータの型を返す関数 (28, 28, 1)
    '''
    return X_DATA_SHAPE[1:]

def get_number_of_classes():
    '''
    クラス数を返す関数
    '''
    return len(LABEL)

def get_label(file=None):
    '''
    ラベルを返す関数
    もし, load_data() を使用していない場合, ラベルが存在しないため外部csv ファイルから呼び出す必要がある
    その際は, file にファイルパスを指定する必要がある
    file : ラベルデータを外部のcsv ファイルから読み込む場合, そのファイルパス
           load_data() にて作成されたラベルが必要な場合, None を渡す必要がある
           デフォルト : None
    return : ラベル(辞書型)
    '''
    global LABEL
    if LABEL is None:
        LABEL = read_dict(file)
    return LABEL

def load_data(validation_split=0.2, samples=1000):
    '''
    __create_label() をもとにqwick draw dataset を読み込む
    validation_split: 全データのうちテストデータの比率
                    　小数点以下切り捨て
    samples: 使用するデータ数 None を指定した場合すべてのデータを返す
    戻り値: (x_train, y_train), (x_test, y_test)
    x_train: 学習に使用する画像データ(*,28,28,1) ndarray
    y_train: 学習に使用するラベル (*) ndarray
    x_test: テストに使用する画像データ (*,28,28,1) ndarray
    y_test: テストに使用するラベル (*) ndarray
    '''
    label = __create_label()
    # 各戻り値を空のnumpy配列で初期化
    x_train = x_test = np.empty(X_DATA_SHAPE)
    y_train = y_test = np.empty(Y_DATA_SHAPE)
    for keys, values in label.items():
        # 元データの読み込み
        data = np.load(FILE_PATH + keys + EXTENSION)
        # 使用するデータ数になるよう調節
        if not samples is None:
            data = data[:samples,]
        # ラベルの作成
        classes = np.ones(shape=data.shape[0], dtype=np.int32)
        classes *= values
        print(keys, values, data.shape, classes.shape)
        # 学習用データの枚数を計算
        train_size = math.floor(len(data)*(1-validation_split))
        # 各戻り値に合うようにデータを追加する
        x_train = np.append(x_train, data[:train_size,]
                .reshape((train_size, 28, 28, 1)), axis=0)
        y_train = np.append(y_train, classes[:train_size,], axis=0)
        x_test = np.append(x_test, data[train_size:,]
                .reshape((len(data) - train_size, 28, 28, 1)), axis=0)
        y_test = np.append(y_test, classes[train_size:,], axis=0)
    return (x_train, y_train), ( x_test, y_test)

def __search_files():
    files = glob.glob(FILE_PATH + "*.npy")
    files = [i.rsplit(".")[-2] for i in files]
    files = [i.rsplit("/")[-1] for i in files]
    return files

def write_csv(file, save_dict):
    '''
    辞書をcsv 形式で書き出す関数
    file : 書き出すファイルパス
    save_dict : 書き出す辞書
    '''
    key_list = [key for key in save_dict.keys()]
    with open(file, "w") as f:
        writer = csv.DictWriter(f, key_list)
        writer.writeheader()
        writer.writerow(save_dict)

def read_dict(file):
    '''
    csv 形式で保存された辞書を読み込む関数
    file : :読み込むcsvファイルのパス
    return : 読み込んだ辞書
    '''
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        l = [row for row in reader]
    return {key:value for key, value in l[0].items()}

def save_info(file, info):
    '''
    文字列データをテキストファイルに書き出す関数
    UTF-8 で保存する
    file : 書き出すファイルパス
    info : 保存したい文字列
    '''
    with open(file, "w", encoding="UTF_8") as f:
        f.write(info)