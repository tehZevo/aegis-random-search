import os
# Suppress some level of logs
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# from tensorflow import logging
# logging.set_verbosity(logging.INFO)

import numpy as np
import json
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
# print("x_train shape:", x_train.shape)
# print(x_train.shape[0], "train samples")
# print(x_test.shape[0], "test samples")

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

def build_model(n_layers, layer_size, activation, lr):
  model = Sequential()
  for i in range(n_layers):
    if i == 0:
      model.add(Dense(layer_size, input_shape=[28*28], activation=activation))
    else:
      model.add(Dense(layer_size, activation=activation))

  model.add(Dense(10, activation="softmax"))

  model.compile(loss="categorical_crossentropy", optimizer=Adam(lr), metrics=["accuracy"])

  return model

# model.summary()

#input is hyperparameters
#output is metrics
def run(n_layers, layer_size, activation, lr):
  #screw it, run this in docker lol
  # keras.backend.clear_session()
  #dont think i can safely clear session as it nukes graphs.. really do have to run this in a separate container lol

  EPOCHS = 1 # for testing
  metrics = {}
  model = build_model(n_layers, layer_size, activation, lr)
  model.fit(x_train, y_train, epochs=EPOCHS, verbose=0)
  #TODO: yes, this should be a separate validation set, but we're testing
  loss, acc = model.evaluate(x_test, y_test)
  metrics["accuracy"] = acc
  metrics["loss"] = loss
  return metrics

metrics = run(1, 32, "relu", 1e-3)

print(json.dumps(metrics))
