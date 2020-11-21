import numpy as np
import pandas as pd
import cv2
import keras
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from keras import models
from keras import layers

path = './Images/'
images = []
steering = []
cnt = 0

df = pd.read_csv("save.csv")

for i in range(len(df)):
    value = df.iloc[i]
    img = cv2.imread(path + str(int(value[1])) + '.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    h, w, _ = img.shape
    roi = img[int(h / 2):h, :, :]
    if np.random.rand() < 0.5:
        roi = cv2.flip(roi, 1)
        val = -value[2])
    roi = roi / 255.
    images.append(roi)
    steering.append(val)
    cnt[val] += 1

for i,v in enumerate(steering):
    if v == -3:
        values[i][0] = 1
    elif v == -2:
        values[i][1] = 1
    elif v == -1:
        values[i][2] = 1
    elif v == 0:
        values[i][3] = 1
    elif v == 1:
        values[i][4] = 1
    elif v == 2:
        values[i][5] = 1
    elif v == 3:
        values[i][6] = 1


images = np.asarray(images)
values = np.asarray(values)
images = images.astype('float32')


X_train, X_test, y_train, y_test = train_test_split(images, values, test_size=0.2, random_state=1)
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.2, random_state=1)


train_datagen = ImageDataGenerator(
    rescale=1. / 255
)

test_datagen = ImageDataGenerator(
    rescale=1. / 255
)

model = models.Sequential()
model.add(layers.Convolution2D(filters=24, kernel_size=5, strides=2, input_shape=X_train[0].shape, activation='elu'))
model.add(layers.Convolution2D(filters=36, kernel_size=5, strides=2, activation='elu'))
model.add(layers.Convolution2D(filters=48, kernel_size=5, strides=2, activation='elu'))
model.add(layers.Convolution2D(filters=64, kernel_size=5, strides=1, activation='elu'))
model.add(layers.Convolution2D(filters=64, kernel_size=5, strides=1, activation='elu'))

model.add(layers.Flatten())
model.add(layers.Dense(units=100, activation='elu'))
model.add(layers.Dense(units=50, activation='elu'))
model.add(layers.Dense(units=10, activation='elu'))
model.add(layers.Dense(units=7, activation='softmax'))

model.compile(Adam(lr=0.0001),
              loss='categorical_crossentropy',
              metrics=['acc'])

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath='model2.h5',
        monitor='val_loss',
        save_best_only=True
    )
]

train_generator = train_datagen.flow(
    X_train,
    y_train,
    batch_size=16
)

validation_generator = test_datagen.flow(
    X_validation,
    y_validation
)

model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator,
    callbacks=callbacks
)

model.save('model.h5')
