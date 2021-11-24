from kivy.lang import Builder
from functools import partial
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from livestream import LiveStream
from mylayoutwidgets import ButtonBinded

class LiveBox(FloatLayout):

    liveStream = ObjectProperty(None)
    status = StringProperty("stop")
    captureButton = ObjectProperty(None)

    def __init__(self, detector = None, model = None, model_properties = None, dbVectors = None, fileNames = None, **kwargs):
        super().__init__(**kwargs)
        # Initialize liveStream
        self.liveStream = LiveStream(detector = detector, model = model, 
        model_properties = model_properties, dbVectors = dbVectors, fileNames = fileNames,
        pos_hint={'center_x':0.5, 'center_y': 0.5}, size_hint = (None, None), size = (640, 480))
        
        self.captureButton = ButtonBinded (text = "Capture", size_hint = (None, None), size = (80, 40))#, pos_hint = {'top': 1, 'right': 1})
        self.captureButton.bind(on_press = self.capture)
        # Align button to video
        self.liveStream.bind(top = (partial(self.captureButton.align_top)), right = (partial(self.captureButton.align_right)))

    def start_live_stream (self, source):
        try:
            self.liveStream.source = source
            self.add_widget(self.liveStream)
            self.add_widget(self.captureButton)
            self.liveStream.reload()
            self.liveStream.state = "play"
            self.status = "play"
        except:
            print ("Error to start live stream...")
    
    def stop_live_stream (self):
        try:
            self.liveStream.state = "stop"
            self.liveStream.source = ""
            self.remove_widget(self.liveStream)
            self.remove_widget(self.captureButton)
            self.status = "stop"
        except Exception as e:
            print ("Error to stop live stream...")
            print (e)

    def capture(self, button):
        self.liveStream.texture.save("test.png", flipped = False)



