from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.uix.floatlayout import MDFloatLayout

from mylayoutwidgets import ColorFloatLayout

Builder.load_file('livebox.kv')

class LiveBox(ColorFloatLayout, HoverBehavior):

    liveStream = ObjectProperty(None)
    liveActionBar = ObjectProperty(None)
    status = StringProperty("stop")

    def __init__(self, detector = None, model = None, model_properties = None, dbVectors = None, fileNames = None, **kwargs):
        super().__init__(**kwargs)
        self.set_live_stream (detector, model, model_properties, dbVectors, fileNames) 
        #Window.bind(mouse_pos=self.on_motion)
    
    # def on_motion(self, window, mouse_pos):
    #     print (str(mouse_pos))
    #     # will receive all motion events.
    #     if self.collide_point(*mouse_pos):
    #         print ('some motion')

    def on_enter(self, *args):
        self.liveActionBar.opacity  = 0.7
        print ('ENTER')

    def on_leave(self, *args):
        self.liveActionBar.opacity  = 0
        print ('LEAVE')

    def set_live_stream (self, detector, model, model_properties, dbVectors, fileNames):
        self.liveStream.detector = detector
        self.liveStream.model = model
        self.liveStream.model_properties = model_properties
        self.liveStream.dbVectors = dbVectors
        self.liveStream.fileNames = fileNames

    def start_live_stream (self, source):
        try:
            self.liveStream.source = source
            self.liveStream.reload()
            self.liveStream.state = "play"
            self.status = "play"
        except:
            print ("Error to start live stream...")
    
    def stop_live_stream (self):
        try:
            self.liveStream.state = "stop"
            self.liveStream.source = ""
            self.status = "stop"
        except Exception as e:
            print ("Error to stop live stream...")
            print (e)

    def adjust_self_size(self, size):
        self.size = size
        self.adjust_livestream_size(size)

    def adjust_livestream_size(self, size):
        factor1 = size[0] / self.liveStream.width
        factor2 = size[1] / self.liveStream.height
        factor = min(factor1, factor2)
        target_size = (int(self.liveStream.width * factor), int(self.liveStream.height * factor))
        self.liveStream.size = target_size     

    def capture_image(self):
        self.liveStream.texture.save("test.png", flipped = False)
