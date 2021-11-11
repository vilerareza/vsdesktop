import io
import os
import threading
import time
from functools import partial

import numpy as np
from cv2 import CascadeClassifier, imread, resize, imdecode
from keras import models
from kivy.graphics import Color, Line
from kivy.graphics.texture import Texture
from kivy.uix.video import Video
from kivy.uix.label import Label

class LiveStream(Video):

    detector = None
    processThisFrame = True
    t_process_frame = None
    target_size = (224, 224, 3)
    modelLocation = "C:/Users/Reza Vilera/.deepface/weights/vgg_face_model_loaded.h5"
    imageDbLocation = "E:/testimages/facetest/facedb/"
    model = None
    filePaths=[]
    fileNames=[]
    dbVectors=[]
    frameCount = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = "stop"
        self.source = ""
        self.texture = Texture.create()
        # Detector
        self.detector = CascadeClassifier("haarcascade_frontalface_default.xml")
        # Recognition
        self.model = models.load_model(self.modelLocation)
        # Create database vectors
        self.filePaths, self.fileNames, self.dbVectors = self.createDatabase()

    # Video Frame Event Function
    def _on_video_frame(self, *largs):
        super()._on_video_frame(*largs)
        # Adjust size according to texture size
        self.size = self.texture.size
        if self.processThisFrame:
            data = io.BytesIO()
            self.texture.save(data, flipped = False, fmt = 'png')
            if self.t_process_frame is None:
                self.t_process_frame = threading.Thread(target = partial(self.process_frame, data))
                self.t_process_frame.start()
        self.frameCount +=1
        if self.frameCount > 20:
            self.frameCount =0
            self.clear_widgets()
            self.canvas.after.clear()

    def process_frame(self, data):
        self.processThisFrame = False
        buff = np.asarray(bytearray(data.read()))
        img = imdecode(buff, 1)
        # # Face detection 
        bboxes = self.detector.detectMultiScale(img)
        if len(bboxes)>0:
            # # Preprocessing
            faces = self.process_face(img, bboxes)
            # # Recognition
            vectors = self.predict(faces, self.model)
            # # Find face label
            faceLabels = self.find_face_label(vectors, self.dbVectors, self.fileNames)
            # # Bounding boxes drawing
            self.clear_widgets()
            self.canvas.after.clear()
            for i in range(len(bboxes)):
                xb, yb, width, height = bboxes[i]
                label = Label(text = faceLabels[i], font_size = 14, font_family = "arial", halign = 'left', valign = 'middle', color = (0,1,0), size_hint = (None, None), size = (100, 40), x = self.x+int(xb), y = self.y+(self.height-int(yb)))
                self.add_widget(label)
                with self.canvas.after:
                    Color (0,0.69,0.31, 0.9)
                    Line(rectangle = (self.x+xb, self.y+(self.height-yb), width, -height), width = 2)
        self.processThisFrame = True
        self.t_process_frame = None

    def process_face(self, img, bboxes):
        faces = []
        for box in bboxes:
            x, y, width, height = box
            face = img[y:y+height,x:x+width,::]
            factor_y = self.target_size[0] / face.shape[0]
            factor_x = self.target_size[1] / face.shape[1]
            factor = min (factor_x, factor_y)
            face = resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
            diff_y = self.target_size[0] - face.shape[0]
            diff_x = self.target_size[1] - face.shape[1]
            # Padding
            face = np.pad(face, ((diff_y//2, diff_y - diff_y//2), (diff_x//2, diff_x-diff_x//2), (0,0)), 'constant')
            face = np.expand_dims(face, axis=0)
            face = face/255
            faces.append(face)
        return faces

    def predict (self, faces, model):
        vectors = []
        for face in faces:
            vector = model.predict(face)[0]#.tolist()
            vectors.append(vector)
        return vectors
    
    def findDistances(self, sampleVector, vectors):
        distances = []
        for vector in vectors:
            # Euclidean distance
            distance = sum(np.power((sampleVector - vector), 2))
            distance = np.sqrt(distance)
            distances.append(distance)
        return distances

    def createDatabase(self):
        files = os.listdir(self.imageDbLocation)
        filePaths = []
        fileNames = []
        dBvectors = []
        for file in files:
            filePath = os.path.join(self.imageDbLocation, file)
            filePaths.append(filePath)
            fileName = os.path.splitext(file)[0]
            fileNames.append(fileName)
            # Reading image from file
            img = imread(filePath)
            # Detect face
            bboxes = self.detector.detectMultiScale(img)
            # first face only
            box = bboxes[0]
            # Preprocess face
            x, y, width, height = box
            face = img[y:y+height,x:x+width,::]
            factor_y = self.target_size[0] / face.shape[0]
            factor_x = self.target_size[1] / face.shape[1]
            factor = min (factor_x, factor_y)
            face = resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
            diff_y = self.target_size[0] - face.shape[0]
            diff_x = self.target_size[1] - face.shape[1]
            # Padding
            face = np.pad(face, ((diff_y//2, diff_y - diff_y//2), (diff_x//2, diff_x-diff_x//2), (0,0)), 'constant')
            face = np.expand_dims(face, axis=0)
            face = face/255
            # Predict vector
            vector = self.model.predict(face)[0]
            dBvectors.append(vector)
        
        return filePaths, fileNames, dBvectors

    def find_face_label(self, faceVectors, dbVectors, nameLabel):
        faceLabels = []
        for vector in faceVectors:
            distances = self.findDistances(vector, dbVectors)
            # faceLabel as a shortest distance
            faceLabel = nameLabel[np.argmin(distances)]
            faceLabels.append(faceLabel)
        return faceLabels
