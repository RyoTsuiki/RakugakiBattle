import numpy as np
import math

FILE_PATH = "../data/"

def __create_list():
    keys = ["car", "cat", "book"]
    values = range(len(keys))
    return dict(zip(keys, values))

def load_data(validation_split=0.2):
    label = __create_list()
    x_train = x_test = np.empty((0,28, 28, 1))
    y_train = y_test = np.empty((0,))
    for keys, values in label.items():
        data = np.load(FILE_PATH + keys + ".npy")
        data = data[:1000,]
        classes = np.ones(shape=data.shape[0], dtype=np.int32)
        classes *= values
        print(keys, values, data.shape, classes.shape)
        train_size = math.floor(len(data)*(1-validation_split))
        x_train = np.append(x_train, data[:train_size,]
                .reshape((train_size, 28, 28, 1)), axis=0)
        y_train = np.append(y_train, classes[:train_size,], axis=0)
        x_test = np.append(x_test, data[train_size:,]
                .reshape((len(data) - train_size, 28, 28, 1)), axis=0)
        y_test = np.append(y_test, classes[train_size:,], axis=0)
    return (x_train, y_train), ( x_test, y_test)

if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = load_data(0.2)
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
