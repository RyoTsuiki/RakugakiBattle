"""quick draw dataset をnumpy形式で読み込むプログラム.

データセットをnumpy 形式で読み込む
指定したファイルパスからデータを読み取る
この時同一ディレクトリ内の.npy ファイルをすべて読み込む
このファイル数は動的に判断し読み込む
その後ラベルも作成する(これも数に依存しない)

このクラスの使用例は train_class.py 参照
"""

import numpy as np
import math
import glob
import csv
import os
import random

class np_load:
    def __init__(self, file_path="./data/"):
        self.X_DATA_SHAPE = (0, 28, 28, 1)
        self.Y_DATA_SHAPE = (0,)
        self.PIXCEL = 28 * 28
        self.EXTENSION = ".npy"
        self.FILE_PATH = file_path
        # os ごとに __search_files() で使用する separator の値を自動で変化させる
        if os.name == "nt": self.separator = "\\" # windows
        else: self.separator = "/" # ubuntu を想定
        # 各data を空のnumpy配列で初期化
        self.x_train = self.x_test = self.x_val = np.empty(self.X_DATA_SHAPE)
        self.y_train = self.y_test = self.y_val = np.empty(self.Y_DATA_SHAPE)

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
        return (self.x_train, self.y_train), (self.x_val, self.y_val), (self.x_test, self.y_test)

    def load(self, train_samples=1000, val_samples=100, test_samples=100, print_flag=True):
        '''
        label をもとにqwick draw dataset を読み込む.
        train_samples: 学習用に使用する画像データの枚数
        val_samples: 検証用に使用する画像データの枚数
        test_samples: テストに使用する画像データの枚数
        print_flag: 進行状況を表示するフラグ. True: 表示 False: 非表示
                    デフォルト: True
        戻り値: (x_train, y_train), (x_test, y_test)
        x_train: 学習に使用する画像データ(*,28,28,1) ndarray
        y_train: 学習に使用するラベル (*) ndarray
        x_train: 検証に使用する画像データ(*,28,28,1) ndarray
        y_train: 検証に使用するラベル (*) ndarray
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
            train = data[:train_samples,]
            val = data[train_samples:(train_samples+val_samples)]
            test = data[(train_samples+val_samples):(train_samples+val_samples+test_samples)]
            # ラベルの作成
            classes = np.ones(shape=(train_samples+val_samples+test_samples), dtype=np.int32)
            classes *= values
            if print_flag:
                print(f"{keys}, {values} : train_shape {train.shape} val_shape {val.shape} test_shape {test.shape}")
            # 各戻り値に合うようにデータを追加する
            self.x_train = np.append(self.x_train, train.reshape((train_samples,) + self.X_DATA_SHAPE[1:]), axis=0)
            self.y_train = np.append(self.y_train, classes[:train_samples], axis=0)
            self.x_val = np.append(self.x_val, val.reshape((val_samples,) + self.X_DATA_SHAPE[1:]), axis=0)
            self.y_val = np.append(self.y_val, classes[:val_samples], axis=0)
            self.x_test = np.append(self.x_test, test.reshape((test_samples,) + self.X_DATA_SHAPE[1:]), axis=0)
            self.y_test = np.append(self.y_test, classes[:test_samples], axis=0)
        # train データのみシャッフル
        idx = list(range(len(self.x_train)))
        random.shuffle(idx)
        x_train = [self.x_train[i] for i in idx]
        y_train = [self.y_train[i] for i in idx]
        self.x_train = np.array(x_train)
        self.y_train = np.array(y_train)
        #print("np_load x", self.x_train.shape)
        #print("np_load y", self.y_train.shape)

        return (self.x_train, self.y_train), (self.x_val, self.y_val), (self.x_test, self.y_test)

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
