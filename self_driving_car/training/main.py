import numpy as np
import pandas as pd
import cv2
import keras
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras import layers

path = './Images/'
images = []
steering = []
cnt = 0

df = pd.read_csv("save.csv")

for i in range(len(df)):
    value = df.iloc[i]
    img = cv2.imread(path+str(cnt)+'.jpg')
    images.append(img)
    steering.append(value[1])
    cnt += 1

images = np.asarray(images)
steering = np.asarray(steering)


X_train, X_test, y_train, y_test = train_test_split(images,steering,test_size=0.25, random_state=1)
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.25, random_state=1)


train_datagen = ImageDataGenerator(
    rescale=1./255,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
)

test_datagen = ImageDataGenerator(
    rescale=1./255
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
model.add(layers.Dense(units=1))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['acc'])

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath='my_model1.h5',
        monitor='val_loss',
        save_best_only=True
    )
]

train_generator = train_datagen.flow(
    X_train,
    y_train,
    batch_size=20
)

validation_generator = test_datagen.flow(
    X_validation,
    y_validation
)

model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator,
    shuffle=1,
    callbacks=callbacks
)