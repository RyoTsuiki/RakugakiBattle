import numpy as np
import math
import glob
import csv
import os

class np_load:
    def __init__(self, file_path="./data/"):
        self.X_DATA_SHAPE = (0, 28, 28, 1)
        self.Y_DATA_SHAPE = (0,)
        self.EXTENSION = ".npy"
        self.FILE_PATH = file_path
        # os ごとに __search_files() で使用する separator の値を自動で変化させる
        if os.name == "nt": self.separator = "\\" # windows
        else: self.separator = "/" # ubuntu を想定
        # 各data を空のnumpy配列で初期化
        self.x_train = self.x_test = np.empty(self.X_DATA_SHAPE)
        self.y_train = self.y_test = np.empty(self.Y_DATA_SHAPE)

    def get_data_shape(self):
        '''
        学習/テストデータの型を返す関数 (28, 28, 1)
        '''
        return self.X_DATA_SHAPE[1:]

    def get_number_of_classes(self, file_path=None):
        '''
        クラス数を返す関数
        もし, ラベルを作成していない場合, ラベルを読み込む必要がある
        その場合, file_path にファイルパスを設定する必要がある
        file_path : ラベルデータを外部のcsv ファイルから読み込む場合, そのファイルパス
                    load_data() にて作成されたラベルが必要な場合, None を渡す必要がある
                    デフォルト : None
        '''
        return len(self.get_label(file_path))

    def get_label(self, file_path=None):
        '''
        ラベルを返す関数
        もし, load_data() を使用していない場合, ラベルが存在しないため外部csv ファイルから呼び出す必要がある
        その際は, file_path にファイルパスを指定する必要がある
        file_path : ラベルデータを外部のcsv ファイルから読み込む場合, そのファイルパス
                    load_data() にて作成されたラベルが必要な場合, None を渡す必要がある
                    デフォルト: None
        return : ラベル(辞書型)
        '''
        if self.label is None: set_label(file_path)
        return self.label

    def get_data(self):
        return (self.x_train, self.y_train), (self.x_test, self.y_test)

    def load(self, validation_split=0.2, samples=1000, print_flag=True):
        '''
        label をもとにqwick draw dataset を読み込む
        validation_split: 全データのうちテストデータの比率
                        　小数点以下切り捨て
        samples: 使用するデータ数 None を指定した場合すべてのデータを返す
        print_flag: 進行状況を表示するフラグ True: 表示 False: 非表示
                    デフォルト: True
        戻り値: (x_train, y_train), (x_test, y_test)
        x_train: 学習に使用する画像データ(*,28,28,1) ndarray
        y_train: 学習に使用するラベル (*) ndarray
        x_test: テストに使用する画像データ (*,28,28,1) ndarray
        y_test: テストに使用するラベル (*) ndarray
        '''
        # ラベルの作成
        keys = self.__search_files()
        values = range(len(keys))
        self.label = dict(zip(keys, values))

        for keys, values in self.label.items():
            # 元データの読み込み
            data = np.load(self.FILE_PATH + keys + self.EXTENSION)
            # 使用するデータ数になるよう調節
            if not samples is None:
                data = data[:samples,]
            # ラベルの作成
            classes = np.ones(shape=data.shape[0], dtype=np.int32)
            classes *= values
            if print_flag: print(keys, values, data.shape, classes.shape)
            # 学習用データの枚数を計算
            train_size = math.floor(len(data)*(1-validation_split))
            # 各戻り値に合うようにデータを追加する
            self.x_train = np.append(self.x_train, data[:train_size,]
                    .reshape((train_size,) + self.get_data_shape()), axis=0)
            self.y_train = np.append(self.y_train, classes[:train_size,], axis=0)
            self.x_test = np.append(self.x_test, data[train_size:,]
                    .reshape((len(data) - train_size,) + self.get_data_shape()), axis=0)
            self.y_test = np.append(self.y_test, classes[train_size:,], axis=0)
        return (self.x_train, self.y_train), (self.x_test, self.y_test)

    def __search_files(self, print_flag=False):
        files = glob.glob(self.FILE_PATH + "*.npy")
        if print_flag: print("after glob", files)
        files = [i.rsplit(".")[-2] for i in files]
        if print_flag: print("after first split", files)
        files = [i.rsplit(self.separator)[-1] for i in files]
        if print_flag: print("after second split", files)
        return files

    def write_csv(self, file_path):
        '''
        辞書をcsv 形式で書き出す関数
        file_path : 書き出すファイルパス
        save_dict : 書き出す辞書
        '''
        key_list = [key for key in self.label.keys()]
        with open(file_path, "w") as f:
            writer = csv.DictWriter(f, key_list)
            writer.writeheader()
            writer.writerow(self.label)

    def set_label(self, file_path):
        '''
        csv 形式で保存された辞書を読み込む関数
        file_path : :読み込むcsvファイルのパス
        return : 読み込んだ辞書
        '''
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            l = [row for row in reader]
        self.label = {key:value for key, value in l[0].items()}

    def save_info(self, file_path, info):
        '''
        文字列データをテキストファイルに書き出す関数
        UTF-8 で保存する
        file_path : 書き出すファイルパス
        info : 保存したい文字列
        '''
        with open(file_path, "w", encoding="UTF_8") as f:
            f.write(info)
