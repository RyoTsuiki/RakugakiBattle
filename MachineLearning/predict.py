from tensorflow.python.keras.models import load_model
import np_load
import numpy as np

model = load_model('my_model.h5')
(x_train, y_train), (x_test, y_test) = np_load.load_data(samples=10)
proba = model.predict_proba(x_test[0].reshape(1, 28, 28, 1))
classes = model.predict_classes(x_test[0].reshape(1, 28, 28, 1))
label = {v: k for k, v in np_load.get_label().items()}
print("スコア:", proba)
print("実際のクラス:", label[y_test[0]])
print(label)
print({classes: score for classes, score in zip(label.values(), proba[0])})
