import os
import json
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from tensorflow import keras

num_classes = 10
input_shape = (28, 28, 1)

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train / 255.
x_test = x_test / 255.
# Make sure images have shape (28, 28, 1)
x_train = x_train.reshape([-1, 28 * 28])
x_test = x_test.reshape([-1, 28 * 28])
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

N_LAYERS = int(os.getenv("N_LAYERS"))
LAYER_SIZE = int(os.getenv("LAYER_SIZE"))
ACTIVATION = os.getenv("ACTIVATION")
LR = float(os.getenv("LR"))

model = Sequential()
for i in range(N_LAYERS):
  if i == 0:
    model.add(Dense(LAYER_SIZE, input_shape=[28*28], activation=ACTIVATION))
  else:
    model.add(Dense(LAYER_SIZE, activation=ACTIVATION))

model.add(Dense(10, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer=Adam(LR), metrics=["accuracy"])

model.summary()

EPOCHS = 1 # for testing

model.fit(x_train, y_train, epochs=EPOCHS)
#TODO: yes, this should be a separate validation set, but we're testing
loss, acc = model.evaluate(x_test, y_test)

metrics = {
  "accuracy": acc,
  "loss": loss
}

print(json.dumps(metrics))
