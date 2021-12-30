import os
import json
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

num_classes = 10
input_shape = (28, 28, 1)

(x_train, y_train), (x_test, y_test) = mnist.load_data()

#preprocess data
x_train = x_train / 255.
x_test = x_test / 255.
x_train = x_train.reshape([-1, 28 * 28])
x_test = x_test.reshape([-1, 28 * 28])
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

#hyperparameters via env vars
N_LAYERS = int(os.getenv("N_LAYERS"))
LAYER_SIZE = int(os.getenv("LAYER_SIZE"))
ACTIVATION = os.getenv("ACTIVATION")
LR = float(os.getenv("LR"))

#create model
model = Sequential()
for i in range(N_LAYERS):
  if i == 0:
    model.add(Dense(LAYER_SIZE, input_shape=[28*28], activation=ACTIVATION))
  else:
    model.add(Dense(LAYER_SIZE, activation=ACTIVATION))

model.add(Dense(10, activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer=Adam(LR), metrics=["accuracy"])
model.summary()

#fit model for one epoch (for demonstration purposes)
model.fit(x_train, y_train, epochs=1)
#yes, this should be a separate validation set, but this is a simple example
loss, acc = model.evaluate(x_test, y_test)

#return metric dict
metrics = {
  "accuracy": acc,
  "loss": loss
}

#last line of stdout is parsed as json and interpreted as the return metrics by random search
print(json.dumps(metrics))
