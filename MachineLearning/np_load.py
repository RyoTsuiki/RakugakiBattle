import numpy as np
import math
import glob

# ファイルパスの指定 (末尾に"/"を入れる)
FILE_PATH = "/home/share/data/"
#FILE_PATH = "../data/"

def get_label():
    '''
    クラス名とそれに対応した値(辞書型)を返す
    keys: class name (English)
    values: 0-len(keys) 読み込んだ順につける
    クラス名はフォルダー内の".npy"ファイルから取得
    戻り値: クラス名とそれに対応した値 (辞書型)
    '''
    keys = __search_files()
    values = range(len(keys))
    return dict(zip(keys, values))

def load_data(validation_split=0.2, samples=1000):
    '''
    __create_list() をもとにqwick draw dataset を読み込む
    validation_split: 全データのうちテストデータの比率
                    　小数点以下切り捨て
    samples: 使用するデータ数 None を指定した場合すべてのデータを返す
    戻り値: (x_train, y_train), (x_test, y_test)
    x_train: 学習に使用する画像データ(*,28,28,1) ndarray
    y_train: 学習に使用するラベル (*) ndarray
    x_test: テストに使用する画像データ (*,28,28,1) ndarray
    y_test: テストに使用するラベル (*) ndarray
    '''
    label = get_label()
    # 各戻り値を空のnumpy配列で初期化
    x_train = x_test = np.empty((0,28, 28, 1))
    y_train = y_test = np.empty((0,))
    for keys, values in label.items():
        # 元データの読み込み
        data = np.load(FILE_PATH + keys + ".npy")
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
    files = [i.rsplit(".")[0] for i in files]
    files = [i.rsplit("/")[-1] for i in files]
    return files

if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = load_data(0.2,1000)
    print("x_train.shape:",x_train.shape)
    print("y_train.shape:",y_train.shape)
    print("x_test.shape:",x_test.shape)
    print("y_test.shape:",y_test.shape)
    print(get_label())
