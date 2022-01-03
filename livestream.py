import io
import threading
import time
from functools import partial

import numpy as np
from cv2 import imdecode, resize

from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.graphics.texture import Texture
from kivy.uix.video import Video
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from attendance.attendanceLayout import AttendanceLayout

Builder.load_file('livestream.kv')

class LiveStream(Video):

    # Vision AI
    aiModel = None
    classes = None
    processThisFrame = True
    t_process_frame = None
    target_size = (224, 224, 3)
    bboxFactor = 0
    frameCount = 0
    streamSize = (640,480)
    attendanceList = ObjectProperty(None)

    def __init__(self, model = None, **kwargs):
        super().__init__(**kwargs)
        self.state = "stop"
        self.source = ""
        self.texture = Texture.create()
        # Vision AI Model
        self.aiModel = model
        self.face = ""
        self.attendanceList = AttendanceLayout()
        self.bind(size = self.calculate_bbox_factor)

    def calculate_bbox_factor(self, *args):
        factor1 = self.width / self.streamSize[0]
        factor2 = self.height / self.streamSize[1]
        self.bboxFactor = min(factor1, factor2)

    # Video Frame Event Function
    def _on_video_frame(self, *largs):
        super()._on_video_frame(*largs)
        # Adjust size according to texture size ?????
        if self.aiModel:
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
        bboxes = self.aiModel.detector.detectMultiScale(img)
        if len(bboxes)>0:
            # # Recognition
            # Check if recognition is True
            print(f'classifier {self.aiModel.classifier}')
            if self.aiModel.classifier:
                 # # Preprocessing
                faces = self.process_face(img, bboxes)
                # # Find face label
                labels = self.predict(faces, self.aiModel.classifier)
                self.attendanceList.add_data(faces, labels)

            # # Bounding boxes drawing
            self.clear_widgets()
            self.canvas.after.clear()
            for i in range(len(bboxes)):
                #xb, yb, width, height = bboxes[i]
                #print (f'ORIGINAL : Xb {xb}, Yb {yb}, width {width}, height {height}')
                xb, yb, width, height = bboxes[i]*self.bboxFactor
                print (f'BBOX FACTOR {self.bboxFactor}, self width {self.width}, {self.height}, Texture Width {self.texture.width},{self.texture.height} Xb {xb}, Yb {yb}, width {width}, height {height}')
                label = Label(text = labels[i], font_size = 16, font_family = "arial", halign = 'left', valign = 'middle', color = (0,0.4,1), size_hint = (None, None), size = (100, 40), x = self.x+int(xb), y = self.y+(self.height-int(yb)))
                self.add_widget(label)
                with self.canvas.after:
                    #Color (0,0.69,0.31, 0.9)
                    Color (0,0.64,0.91, 1.0)
                    Line(rectangle = (self.x+xb, self.y+(self.height-yb), width, -height), width = 1.5)
            
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
            face = np.moveaxis(face, -1, 1)
            faces.append(face)
        return faces

    def predict (self, faces, model, model_properties=None):
        pass
        try:
            labels = []
            for face in faces:
                face = np.moveaxis(face,1,-1)
                vector = model.predict(face)
                vector = vector.argmax(axis = -1)
                label = self.aiModel.label.inverse_transform(vector)
                label = label[0]
                labels.append(label)
            print(f'labels : {labels}')
            return labels
        except Exception as e:
            print ("Something happen during predict")
            print (e)
    
