from tensorflow.python.keras.datasets import cifar10
from tensorflow.python.keras.utils import to_categorical
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import MaxPooling2D
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.callbacks import TensorBoard
from sklearn.metrics import confusion_matrix
import numpy as np

# データのインポート
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

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
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
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
        input_shape=(32, 32, 3),
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
        units=10,
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

## TensorBoard のパス
tsb = TensorBoard(log_dir="./logs/20190613-1")

## 学習
## https://www.tensorflow.org/api_docs/python/tf/keras/models/Model#fit
history_model = model.fit(
    x_train,
    y_train,
    # 勾配更新ごとのサンプル数
    batch_size=32,
    # モデルを訓練するためのエポック数
    epochs=2,
    # 検証データとして使用するトレーニングデータの割合
    validation_split=0.2,
    # コールバック関数 TensorBoard を使用する
    callbacks=[tsb]
)

# 結果の表示
score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# 予測
predict_classes = model.predict_classes(x_test, batch_size=32)
true_classes = np.argmax(y_test,1)
print(confusion_matrix(true_classes, predict_classes))
