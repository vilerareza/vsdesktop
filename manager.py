import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

import numpy as np
from cv2 import CascadeClassifier, imread, resize
from openvino.inference_engine import IECore

Builder.load_file('manager.kv')

class Manager(BoxLayout):

    headerBar = ObjectProperty(None)
    mainTabs = ObjectProperty (None)
    
    detector = None
    model = None
    modelLocation = "E:/testimages/facetest/vggface/ir/saved_model.xml"
    imageDbLocation = "E:/testimages/facetest/facedb/"
    filePaths=[]
    fileNames=[]
    dbVectors=[]
    model_properties = []
    newTabs = []
    
    orientation = "vertical"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_main_tabs()

    def move_main_tabs(self):
        ''' Move main tabs to header bar'''
        # Copy the original tabs
        self.newTabs = self.mainTabs.tab_list.copy()
        # Remove the original tabs
        self.mainTabs.clear_tabs()
        self.mainTabs.tab_height = 0
        # Put the copy of original tabs in the 
        for newTab in reversed(self.newTabs):
            # Styling
            if newTab == self.mainTabs.ids.id_tab_setting_view:
                newTab.size_hint = (None, None)
                newTab.size = (dp(60), dp(40))
                newTab.background_normal = 'images/tab_setting_normal.png'
                newTab.background_down = 'images/tab_setting_down.png'
                self.headerBar.tabStrip.add_widget(newTab)
            elif newTab == self.mainTabs.ids.id_tab_multi_view:
                newTab.size_hint = (None, None)
                newTab.size = (dp(60), dp(40))
                newTab.background_normal = 'images/tab_multiview_normal.png'
                newTab.background_down = 'images/tab_multiview_down.png'
                self.headerBar.tabStrip.add_widget(newTab)

    def stop(self):
        self.mainTabs.stop()

    def activate_vision_ai(self):
        # Face detector
        self.detector = CascadeClassifier("haarcascade_frontalface_default.xml")
        # Recognition
        # Keras model
        #self.model = models.load_model(self.modelLocation)
        # INFERENCE ENGINE
        ie = IECore()
        net  = ie.read_network(model = self.modelLocation)
        input_name = next(iter(net.input_info))
        output_name = next(iter(net.outputs))
        self.model_properties = input_name, output_name
        try:
            self.model = ie.load_network(network = self.modelLocation, device_name = "MYRIAD")
            print ("USE NCS2 VPU")
        except:
            self.model = ie.load_network(network = self.modelLocation, device_name = "CPU")
            print ("NCS2 not found, use CPU...")
        # Create database vectors
        self.filePaths, self.fileNames, self.dbVectors = self.createDatabase()

    def createDatabase(self):
        files = os.listdir(self.imageDbLocation)
        filePaths = []
        fileNames = []
        dBvectors = []
        target_size = (224, 224, 3)
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
            factor_y = target_size[0] / face.shape[0]
            factor_x = target_size[1] / face.shape[1]
            factor = min (factor_x, factor_y)
            face = resize(face, (int(face.shape[0]* factor), int(face.shape[1]*factor)))
            diff_y = target_size[0] - face.shape[0]
            diff_x = target_size[1] - face.shape[1]
            # Padding
            face = np.pad(face, ((diff_y//2, diff_y - diff_y//2), (diff_x//2, diff_x-diff_x//2), (0,0)), 'constant')
            face = np.expand_dims(face, axis=0)
            face = face/255
            face = np.moveaxis(face, -1, 1)
            # Predict vector
            result = self.model.infer({self.model_properties[0]: face})
            output = result[self.model_properties[1]]
            vector = output[0]
            #vector = self.model.predict(face)[0]
            dBvectors.append(vector)
        
        return filePaths, fileNames, dBvectors