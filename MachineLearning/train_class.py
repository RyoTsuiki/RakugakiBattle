"""学習を行うプログラム.

quick draw dataset を用いて学習を行うクラス
このクラスを使用して学習を実行する(このプログラムだけでは学習しない)
np_load_class.py を使用する
np_load_class を使用するためには事前にデータを取得する必要がある
もし, 異なるデータセットを使用する場合は, np_load_class を新たに作成すればよい
同様の関数を作成すれば, ピクセル値(今回は28*28) が変更してもモデルを特に変更する必要はない(はず)

実際に使用したコード(例)
Colaboratory を使用

# Google ドライブをマウントするには、このセルを実行してください。
from google.colab import drive
drive.mount('/content/gdrive')
%cd "/content/gdrive/My Drive/Colab Notebooks/exp5"

import sys
sys.path.append("/content/gdrive/My Drive/Colab Notebooks/exp5/prog")
import np_load_class as np
import train_class as tr

lr = [1e-5, 1e-2]
data = np.np_load("/content/gdrive/My Drive/Colab Notebooks/exp5/top10/")
data.load(train_samples=50000, val_samples=0, test_samples=10000)
for i in lr:
  cnn = tr.Train()
  cnn.set_model_parameter(epochs=100, firstlr=i)
  cnn.set_save_parameter(folder_name="class_10/" + str(i))
  cnn.set_data(data)
  cnn.train()
  data.write_csv("class_10/" + str(i) + "/label.csv")
"""


import datetime
import time
from tensorflow.python.keras.utils import to_categorical
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import MaxPooling2D
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.callbacks import TensorBoard, ReduceLROnPlateau, CSVLogger
from tensorflow.python.keras.models import save_model, load_model
from tensorflow.python.keras.optimizers import Adam
#from sklearn.metrics import confusion_matrix
from sklearn.metrics import *
import numpy as np
import matplotlib.pyplot as plt


class Train:
    def set_model_parameter(self, epochs=20, split=0.2, samples=1000, firstlr=0.001, callbacs=[], verbose=2):
        self.epochs = epochs
        self.split = split
        self.samples = samples
        self.firstlr = firstlr
        self.callbacks = callbacs
        self.verbose = verbose

    def set_save_parameter(self, folder_pass="./", folder_name=None, tsb_flag=True,
                           csvlog_flag=True, model_flag=True, info_flag=True, fig_flag=True):
        self.folder_pass = folder_pass
        self.folder_name = folder_name
        if self.folder_name is None:
            date = datetime.datetime.now()
            self.folder_name = "{0:%Y_%m_%d_%H_%M_%S}".format(date)
        if tsb_flag:
            tsb = TensorBoard(log_dir=self.folder_pass+self.folder_name+"/log")
            self.callbacks.append(tsb)
        if csvlog_flag:
            csv_logger = CSVLogger(
                filename=self.folder_pass+folder_name+"/log.csv", separator=',', append=True)
            self.callbacks.append(csv_logger)
        self.model_flag = model_flag
        self.info_flag = info_flag
        self.fig_flag = fig_flag

    def set_data(self, data=None, print_flag=True):
        """
        data をセットするメソッド
        data: np_load のインスタンス
              あらかじめ np_load.load() を実行しておく必要がある
        print_flag: 読み込んだデータの大きさを表示するフラグ
                    True: 表示, False: 非表示
                    デフォルト: True
        """
        (x_train, y_train), (x_val, y_val), (x_test, y_test) = data.get_data()
        self.x_train = x_train
        self.y_train = y_train
        self.x_val = x_val
        self.y_val = y_val
        self.x_test = x_test
        self.y_test = y_test
        self.data = data
        if print_flag:
            print("x_train.shape:", self.x_train.shape)
            print("x_val.shape:", self.x_val.shape)
            print("x_test.shape:", self.x_test.shape)

            print("y_train.shape:", self.y_train.shape)
            print("y_val.shape:", self.y_val.shape)
            print("y_test.shape:", self.y_test.shape)

    def __pre(self):
        """
        データの前処理
        """
        # 特徴量の正規化
        self.x_train = self.x_train/255.
        self.x_test = self.x_test/255.
        # クラスベクトルの1-hot ベクトル化
        self.y_train = to_categorical(
            self.y_train, self.data.get_number_of_classes())
        self.y_val = to_categorical(
            self.y_val, self.data.get_number_of_classes())
        self.y_test = to_categorical(
            self.y_test, self.data.get_number_of_classes())

    def __build_model(self):
        # モデル構築の準備
        self.model = Sequential()

        # 畳み込み層の追加 (1層目)
        self.model.add(
            Conv2D(
                # 出力チャンネル数(特徴マップの数)
                filters=32,
                # 入力されるテンソルの形
                input_shape=self.data.get_data_shape(),
                # カーネルの大きさ 3*3 or 5*5 奇数にする
                kernel_size=(3, 3),
                # カーネルをずらす幅
                strides=(1, 1),
                # データの端をどのように扱うかを指定
                # 今回は入力と出力のサイズを一致させるためsame を使用
                padding='same',
                # 活性化関数の種類 (ReLU 関数は収束が早いらしい)
                activation='relu'
            )
        )

        # 畳み込み層の追加 (2層目)
        # 2層目以降はkeras がinput_shape を自動計算するため省略可能
        self.model.add(
            Conv2D(
                # 出力チャンネル数(特徴マップの数)
                filters=32,
                # カーネルの大きさ 3*3 or 5*5 奇数にする
                kernel_size=(3, 3),
                # カーネルをずらす幅
                strides=(1, 1),
                # データの端をどのように扱うかを指定
                # 今回は入力と出力のサイズを一致させるためsame を使用
                padding='same',
                # 活性化関数の種類 (ReLU 関数は収束が早いらしい)
                activation='relu'
            )
        )

        # プーリング層の追加
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        # ドロップアウトレイヤーの追加
        self.model.add(Dropout(0.25))

        # 畳み込み層の追加 (3層目)
        # 2層目以降はkeras がinput_shape を自動計算するため省略可能
        self.model.add(
            Conv2D(
                # 出力チャンネル数(特徴マップの数)
                filters=64,
                # カーネルの大きさ 3*3 or 5*5 奇数にする
                kernel_size=(3, 3),
                # カーネルをずらす幅
                strides=(1, 1),
                # データの端をどのように扱うかを指定
                # 今回は入力と出力のサイズを一致させるためsame を使用
                padding='same',
                # 活性化関数の種類 (ReLU 関数は収束が早いらしい)
                activation='relu'
            )
        )

        # 畳み込み層の追加 (4層目)
        # 2層目以降はkeras がinput_shape を自動計算するため省略可能
        self.model.add(
            Conv2D(
                # 出力チャンネル数(特徴マップの数)
                filters=64,
                # カーネルの大きさ 3*3 or 5*5 奇数にする
                kernel_size=(3, 3),
                # カーネルをずらす幅
                strides=(1, 1),
                # データの端をどのように扱うかを指定
                # 今回は入力と出力のサイズを一致させるためsame を使用
                padding='same',
                # 活性化関数の種類 (ReLU 関数は収束が早いらしい)
                activation='relu'
            )
        )

        # プーリング層の追加
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        # ドロップアウトレイヤーの追加
        self.model.add(Dropout(0.25))

        # Flattenレイヤーの追加
        # 多次元のテンソルを2次元のテンソルに展開
        self.model.add(Flatten())

        # 全結合層の追加
        self.model.add(
            Dense(
                # ニューロンの数 (出力次元)
                units=512,
                # 活性化関数
                activation='relu'
            )
        )

        # ドロップアウトレイヤーの追加
        self.model.add(Dropout(0.25))

        # 全結合層の追加
        self.model.add(
            Dense(
                # ニューロンの数 (出力次元)
                units=self.data.get_number_of_classes(),
                # 活性化関数
                activation='softmax'
            )
        )

    def train(self):
        self.__pre()
        self.__build_model()
        # モデルのコンパイル
        self.model.compile(
            # 最適化アルゴリズム
            optimizer=Adam(lr=self.firstlr),
            # 損失関数 交差エントロピー多値分類
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        # 時間の計測
        start = time.time()
        # 学習
        self.history_model = self.model.fit(
            self.x_train,
            self.y_train,
            # 勾配更新ごとのサンプル数
            batch_size=32,
            # モデルを訓練するためのエポック数
            epochs=self.epochs,
            # 検証データとして使用するトレーニングデータの割合
            validation_split=self.split,
            # 検証用データの指定
            #validation_data=(self.x_val, self.y_val),
            # シャッフル
            shuffle=True,
            # 表示設定
            verbose=self.verbose,
            # コールバック関数 TensorBoard を使用する
            callbacks=self.callbacks
            # コールバック関数 学習率も変化させる場合
            #callbacks=[tsb, reduce_lr]
        )
        # 時間の計測 ここまで
        self.elapsed_time = time.time() - start
        # 予測
        self.predict_classes = self.model.predict_classes(
            self.x_test, batch_size=32)
        self.true_classes = np.argmax(self.y_test, 1)
        # 保存
        if self.model_flag:
            self.model.save(self.folder_pass+self.folder_name+"/model.h5")
            print("save model")
        if self.info_flag:
            self.data.save_info(
                self.folder_pass+self.folder_name+"/info.txt", self.__create_info())
            print("save info")
        if self.fig_flag:
            self.save_fig()

    def __create_info(self):
        info = "-"*10 + "info" + "-"*10 + "\n"
        info += f"{self.data.get_label()}\n"
        info += f"train : {self.y_train.shape[0]*(1-self.split)}\n"
        info += f"validation : {self.y_train.shape[0]*self.split}\n"
        info += f"test : {self.y_test.shape[0]} \n"
        info += f"epochs : {self.epochs} \n"
        info += f"lr : {self.firstlr} \n"
        #info += f"call backs : {CALLBACKSLIST} \n"
        info += f"学習時間 : {self.elapsed_time / 60}(min) \n"
        #info += f"保存フォルダー先: {folder}\n"
        #info += "-"*10 + "Verification　eval" + "-"*10 + "\n"
        #info += f"loss: {score[0]} \n"
        #info += f"accuracy: {score[1]} \n"
        info += "-"*10 + "test eval" + "-"*10 + "\n"
        info += f"正答率: {accuracy_score(self.true_classes, self.predict_classes)}\n"
        info += f"混同行列\n{confusion_matrix(self.true_classes, self.predict_classes)}\n"
        return info

    def print_info(self):
        print(self.__create_info())

    def save_fig(self):
        plt.plot(range(1, self.epochs+1),
                 self.history_model.history['acc'], label="training")
        plt.plot(range(1, self.epochs+1),
                 self.history_model.history['val_acc'], label="validation")
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        # plt.show()
        plt.savefig(self.folder_pass+self.folder_name+'/Accuracy.png')

        plt.clf()

        plt.plot(range(1, self.epochs+1),
                 self.history_model.history['loss'], label="training")
        plt.plot(range(1, self.epochs+1),
                 self.history_model.history['val_loss'], label="validation")
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        # plt.show()
        plt.savefig(self.folder_pass+self.folder_name+'/Loss.png')

        plt.clf()
