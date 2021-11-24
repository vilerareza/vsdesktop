import os
import time

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.graphics import Color, Rectangle

from mylayoutwidgets import LogoBar
from settingview import SettingView
from multiview import Multiview

import numpy as np
from cv2 import CascadeClassifier, imread, resize
from openvino.inference_engine import IECore

class Manager(BoxLayout):

    detector = None
    model = None
    modelLocation = "E:/testimages/facetest/vggface/ir/saved_model.xml"
    imageDbLocation = "E:/testimages/facetest/facedb/"
    filePaths=[]
    fileNames=[]
    dbVectors=[]
    model_properties = []

    tabs = ObjectProperty
    
    orientation = "vertical"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Logo bar
        self.logoBar = LogoBar(size_hint = (1,None), height = 30)
        # Adding image, original size is 300x78
        self.logoBar.add_widget(Image(source = "images/vs_logo2.png", pos_hint = {'left': 1, 'top': 1}, size_hint = (None, 1), width = 130))
        self.add_widget(self.logoBar)
        # Adding Tabs Panel
        self.tabs = VsDesktopTabs()
        self.add_widget(self.tabs)
    
    def stop(self):
        self.tabs.stop()

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


class VsDesktopTabs(TabbedPanel):
    multiView = ObjectProperty()
    settingView = ObjectProperty()
    tabMultiView = ObjectProperty()
    tabSettingView = ObjectProperty()

    do_default_tab = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiView = Multiview()
        self.settingView = SettingView()
        self.tabSettingView = TabbedPanelItem(content = self.settingView, text = "Settings")
        self.tabMultiView = TabbedPanelItem(content = self.multiView, text = "Multiview")
        self.add_widget(self.tabSettingView)
        self.add_widget(self.tabMultiView)
        self.tabSettingView.bind(on_press=self.tabSettingViewPressed)
        self.tabMultiView.bind(on_press=self.refreshMultiView)
    
    def tabSettingViewPressed(self, tab):
        if tab.state == "down":
            # Stop the multiview
            self.multiView.stop()
    
    def refreshMultiView(self, tab):
        if tab.state == "down":
            # Refresh the device list
            self.multiView.get_items_from_db()
            self.multiView.start_icons()
            
    def stop(self):
        self.multiView.stop()