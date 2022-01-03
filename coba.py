from tensorflow.keras.models import load_model
import cv2
from numpy import asarray
import numpy as np

img = cv2.imread('files/coba.png')
img = asarray(img)
print(img.shape)
x_test = np.expand_dims(img, axis=0).astype('float32')
print(x_test.shape)
modelLocation = 'files/vromeo_ai_model.h5'
model = load_model(modelLocation, compile=False)
y = model.predict(x_test)
print(y)
print(model)