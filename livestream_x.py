import os
import threading
from functools import partial
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.graphics.texture import Texture
from kivy.uix.video import Video
from kivy.properties import ObjectProperty
import io
import cv2 as cv
from cv2 import imdecode, rectangle
#import face_recognition
from cv2 import CascadeClassifier
#import mtcnn
import numpy as np
from keras import models
import time


class LiveStream(Video):

    box_width = 50
    box_height = 50
    boundingBox = ObjectProperty(None)
    detector = None
    fileName = "images/reza1.jpg"
    known_encoding = []
    known_names = []
    face_locations = []
    face_encodings = []
    processThisFrame = True
    t_process_frame = None
    target_size = (224, 224, 3)
    modelLocation = "C:/Users/Reza Vilera/.deepface/weights/vgg_face_model_loaded.h5"
    imageDbLocation = "E:/testimages/facetest/facedb/"
    model = None
    filePaths=[]
    fileNames=[]
    dBvectors=[]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = "stop"
        self.source = ""
        self.texture = Texture.create()
        
        # Cascade
        self.detector = CascadeClassifier("haarcascade_frontalface_default.xml")
        # MTCNN
        #self.detector = mtcnn.MTCNN()

        # Recognition
        self.model = models.load_model(self.modelLocation)
        # face_recognition
        # person1_img = face_recognition.load_image_file(self.fileName)
        # person1_encoding = face_recognition.face_encodings(person1_img)
        # self.known_encoding = [person1_encoding]
        # self.known_names= ["Reza"]
        self.filePaths, self.fileNames, self.dBvectors = self.createDatabase()
    #     with self.canvas.after:
    #         Color (0,1,0)
    #         self.boundingBox = Line(points = [self.center_x - self.box_width/2, self.center_y + self.box_height/2, self.center_x + self.box_width/2, self.center_y + self.box_height/2,
    #         self.center_x + self.box_width/2, self.center_y - self.box_height/2,
    #         self.center_x - self.box_width/2, self.center_y - self.box_height/2,
    #         self.center_x - self.box_width/2, self.center_y + self.box_height/2], width = 2)
    #         self.bind (pos = self.update_box, size = self.update_box)

    # def update_box(self, *args):
    #     self.boundingBox.points = [self.center_x - self.box_width/2, self.center_y + self.box_height/2, self.center_x + self.box_width/2, self.center_y + self.box_height/2,
    #     self.center_x + self.box_width/2, self.center_y - self.box_height/2,
    #     self.center_x - self.box_width/2, self.center_y - self.box_height/2,
    #     self.center_x - self.box_width/2, self.center_y + self.box_height/2]

    # CASCADE THREAD
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

    def process_frame(self, data):
        self.processThisFrame = False
        buff = np.asarray(bytearray(data.read()))
        img = imdecode(buff, 1)
        # # Face detection happens here
        bboxes = self.detector.detectMultiScale(img)
        # # Bounding boxes drawing
        self.canvas.after.clear()
        for bbox in bboxes:
            x, y, width, height = bbox
            with self.canvas.after:
                Color (0,0.69,0.31, 0.9)
                Line(rectangle = (self.x+x, self.y+(self.height-y), width, -height), width = 2)
        # # Recognition happens here
        faces = self.process_face(img, bboxes)
        vectors = self.predict(faces, self.model)
        for vector in vectors:
            self.findDistances(vector, self.dBvectors)
        self.processThisFrame = True
        self.t_process_frame = None

    # CASCADE NORMAL
    # def _on_video_frame(self, *largs):
    #     super()._on_video_frame(*largs)
    #     # Adjust size according to texture size
    #     self.size = self.texture.size
    #     if self.processThisFrame:
    #         # Save and convert texture to numpy array
    #         self.process_frame(self.texture)

    # def process_frame(self, texture):
    #     self.processThisFrame = False
    #     # Save and convert texture to numpy array
    #     data = io.BytesIO()
    #     texture.save(data, flipped = False, fmt = 'png')
    #     buff = np.asarray(bytearray(data.read()))
    #     img = imdecode(buff, 1)
    #     # # Face detection happens here
    #     bboxes = self.detector.detectMultiScale(img)
    #     # # Bounding boxes drawing
    #     self.canvas.after.clear()
    #     for bbox in bboxes:
    #         x, y, width, height = bbox
    #         with self.canvas.after:
    #             Color (0,0.69,0.31, 0.9)
    #             Line(rectangle = (self.x+x, self.y+(self.height-y), width, -height), width = 2)
    #     self.processThisFrame = True

    # def process_frame(self, texture):
    #     self.processThisFrame = False
    #     # Save and convert texture to numpy array
    #     data = io.BytesIO()
    #     self.texture.save(data, flipped = False, fmt = 'png')
    #     buff = np.asarray(bytearray(data.read()))
    #     img = imdecode(buff, 1)
    #     # Face detection happens here
    #     faces = self.detector.detect_faces(img)
    #     # Bounding boxex drawing
    #     self.canvas.after.clear()
    #     for face in faces:
    #         x, y, width, height = face['box']
    #         with self.canvas.after:
    #             Color (0,0.69,0.31, 0.9)
    #             print(str(self.x) +", "+str(x))
    #             Line(rectangle = (self.x+x, self.y+y, width, height), width = 2)
    #     self.processThisFrame = True

    # MTCNN NORMAL
    # def _on_video_frame(self, *largs):
    #     super()._on_video_frame(*largs)
    #     # Adjust size according to texture size
    #     self.size = self.texture.size
    #     # Save and convert texture to numpy array
    #     data = io.BytesIO()
    #     self.texture.save(data, flipped = False, fmt = 'png')
    #     buff = np.asarray(bytearray(data.read()))
    #     img = imdecode(buff, 1)
    #     # Face detection happens here
    #     faces = self.detector.detect_faces(img)
    #     # Bounding boxex drawing
    #     self.canvas.after.clear()
    #     for face in faces:
    #         x, y, width, height = face['box']
    #         with self.canvas.after:
    #             Color (0,0.69,0.31, 0.9)
    #             print(str(self.x) +", "+str(x))
    #             Line(rectangle = (self.x+x, self.y+(self.height-y), width, -height), width = 2)
    
    # MTCNN THREAD
    # def _on_video_frame(self, *largs):
    #     super()._on_video_frame(*largs)
    #     # Adjust size according to texture size
    #     self.size = self.texture.size
    #     # Save and convert texture to numpy array
    #     if self.processThisFrame:
    #         data = io.BytesIO()
    #         self.texture.save(data, flipped = False, fmt = 'png')
    #         if self.t_process_frame is None:
    #             self.t_process_frame = threading.Thread(target = partial(self.process_frame, data))
    #             self.t_process_frame.start()

    # def process_frame(self, data):
    #     self.processThisFrame = False
    #     buff = np.asarray(bytearray(data.read()))
    #     img = imdecode(buff, 1)
    #     # Face detection happens here
    #     faces = self.detector.detect_faces(img)
    #     # Bounding boxex drawing
    #     self.canvas.after.clear()
    #     for face in faces:
    #         x, y, width, height = face['box']
    #         with self.canvas.after:
    #             Color (0,0.69,0.31, 0.9)
    #             Line(rectangle = (self.x+x, self.y+(self.height-y), width, -height), width = 2)
    #     self.processThisFrame = True
    #     self.t_process_frame = None


    #face_recognition
    # def _on_video_frame(self, *largs):
    #     super()._on_video_frame(*largs)
    #     # Adjust size according to texture size
    #     self.size = self.texture.size
    #     # Save and convert texture to numpy array
    #     data = io.BytesIO()
    #     self.texture.save(data, flipped = False, fmt = 'png')
    #     buff = np.asarray(bytearray(data.read()))
    #     img = imdecode(buff, 1)
    #     # Face detection happens here
    #     self.face_locations = face_recognition.face_locations(img, model = "hog")
    #     # # Bounding boxes drawing
    #     self.canvas.after.clear()
    #     for face_location in self.face_locations:
    #         bottom, right, top, left = face_location
    #         with self.canvas.after:
    #             Color (0,0.69,0.31, 0.9)
    #             Line(rectangle = (self.x+left, self.y+bottom, right-left, top-bottom), width = 2)
    #             print (str(top-bottom))

    def process_face(self, img, bboxes):
        faces = []
        for box in bboxes:
            x, y, width, height = box
            face = img[y:y+height,x:x+width,::]
            factor_y = self.target_size[0] / face.shape[0]
            factor_x = self.target_size[1] / face.shape[1]
            factor = min (factor_x, factor_y)
            face = cv.resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
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
            img = cv.imread(filePath)
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
            face = cv.resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
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