import np_load
import datetime
from tensorflow.python.keras.utils import to_categorical
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import MaxPooling2D
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.models import save_model, load_model
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import numpy as np

#パラメータの定義

EPOCHS = 40
SPLIT = 0.2
SAMPLES = 1000

# パラメータの定義 ここまで

# データのインポート
(x_train, y_train), (x_test, y_test) = np_load.load_data(samples=SAMPLES)

# データの整形
## データの大きさを確認
print("x_train.shape:", x_train.shape)
print("x_test.shape:", x_test.shape)
print("y_train.shape:", y_train.shape)
print("y_test.shape:", y_test.shape)

## 特徴量の正規化
x_train = x_train/255.
x_test = x_test/255.

## クラスベクトルの1-hot ベクトル化
y_train = to_categorical(y_train, np_load.get_number_of_classes())
y_test = to_categorical(y_test, np_load.get_number_of_classes())
print("(after 1-hot)y_train.shape:", y_train.shape)
print("(after 1-hot)y_test.shape:", y_test.shape)


# モデル構築
## モデル構築の準備
model = Sequential()

## 畳み込み層の追加 (1層目)
model.add(
    Conv2D(
        # 出力チャンネル数(特徴マップの数)
        filters=32,
        # 入力されるテンソルの形
        input_shape=np_load.get_data_shape(),
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

## 畳み込み層の追加 (2層目)
## 2層目以降はkeras がinput_shape を自動計算するため省略可能
model.add(
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

## プーリング層の追加
model.add(MaxPooling2D(pool_size=(2, 2)))

## ドロップアウトレイヤーの追加
model.add(Dropout(0.25))

## 畳み込み層の追加 (3層目)
## 2層目以降はkeras がinput_shape を自動計算するため省略可能
model.add(
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

## 畳み込み層の追加 (4層目)
## 2層目以降はkeras がinput_shape を自動計算するため省略可能
model.add(
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

## プーリング層の追加
model.add(MaxPooling2D(pool_size=(2, 2)))

## ドロップアウトレイヤーの追加
model.add(Dropout(0.25))

## 全結合層の追加
### プーリング層追加後のモデルの出力形式
print(model.output_shape)

## Flattenレイヤーの追加
## 多次元のテンソルを2次元のテンソルに展開
model.add(Flatten())
print(model.output_shape)

## 全結合層の追加
model.add(
    Dense(
        # ニューロンの数 (出力次元)
        units=512,
        # 活性化関数
        activation='relu'
    )
)

## ドロップアウトレイヤーの追加
model.add(Dropout(0.25))

## 全結合層の追加
model.add(
    Dense(
        # ニューロンの数 (出力次元)
        units=np_load.get_number_of_classes(),
        # 活性化関数
        activation='softmax'
    )
)

# モデルを学習する
## モデルのコンパイル
model.compile(
    # 最適化アルゴリズム
    optimizer="adam",
    # 損失関数 交差エントロピー多値分類
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# 保存するファイルのパス作成
date = datetime.datetime.now()
folder = "{0:%Y_%m_%d_%H_%M_%S}".format(date)
## TensorBoard のパス
tsb = TensorBoard(log_dir="./" + folder + "/log")

## 学習係数を下げる
## https://keras.io/callbacks/
#reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

# 学習率 https://blog.shikoan.com/keras-learning-rate-decay/
def step_decay(epoch):
    x = 0.1
    if epoch >= 30: x = 0.01
    if epoch >= 70: x = 0.001
    return x
reduce_lr = LearningRateScheduler(step_decay)

## 学習
## https://www.tensorflow.org/api_docs/python/tf/keras/models/Model#fit
history_model = model.fit(
    x_train,
    y_train,
    # 勾配更新ごとのサンプル数
    batch_size=32,
    # モデルを訓練するためのエポック数
    epochs=EPOCHS,
    # 検証データとして使用するトレーニングデータの割合
    validation_split=SPLIT,
    # コールバック関数 TensorBoard を使用する
    callbacks=[tsb]
    # コールバック関数 学習率も変化させる場合
    #callbacks=[tsb, reduce_lr]
)

# 結果の表示
score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# モデルの保存
FILE_PATH = "my_model.h5"
model.save(FILE_PATH)

# 予測
predict_classes = model.predict_classes(x_test, batch_size=32)
true_classes = np.argmax(y_test,1)
info = "-"*10 + "info" + "-"*10 + "\n"
print("-"*10 + "info" + "-"*10)
info += f"{LABEL}\n"
print(LABEL)
info += f"train : {y_train.shape[0]*(1-SPLIT)}\n"
print("train :", y_train.shape[0]*(1-SPLIT))
info += f"validation : {y_train.shape[0]*SPLIT}\n"
print("validation :", y_train.shape[0]*SPLIT)
info += f"test : {y_test.shape[0]} \n"
print("test :", y_test.shape[0])
info += f"epochs : {EPOCHS} \n"
print("epochs :", EPOCHS)
info += f"保存フォルダー先: {folder}\n"
print("保存フォルダー先:",folder)
info += "-"*10 + "test eval" + "-"*10 + "\n"
print("-"*10 + "test eval" + "-"*10)
info += f"正答率: {accuracy_score(true_classes, predict_classes)}\n"
print("正答率:",accuracy_score(true_classes, predict_classes))
info += f"混同行列\n{confusion_matrix(true_classes, predict_classes)}\n"
print("混同行列\n", confusion_matrix(true_classes, predict_classes))
np_load.save_info(folder + "/info.txt", info)
