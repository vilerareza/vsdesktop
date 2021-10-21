import threading
from threading import Condition
from kivy.app import App, ObjectProperty
from kivy.core.video import video_ffpyplayer
from kivy.graphics import Color, Rectangle
from kivy.loader import Loader
from kivy.network.urlrequest import UrlRequest
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.app import App
from kivy.graphics.texture import Texture
import random

class multiSelectionItem(Image):
    camera_url = None
    isEnabled = BooleanProperty(True)
    t_status_checker = None
    condition = Condition()
    request_param_check = "?check"
    request_param_start = "?start"
    request_param_stop = "?stop"
    stop_flag = False

    def check_camera(self):
        print ('check camera')
        req = UrlRequest(url=(self.camera_url+self.request_param_check), on_success = self.callback_ok, timeout=2, on_error = self.callback_fail, on_failure = self.callback_fail)
        
    def check(self):
        while (not self.stop_flag):
            # if the application exit then break the loop
            with self.condition:
                if not (self.condition.wait(timeout = 2)):
                    # Timeout. No frame detected
                    self.check_camera()

    def callback_ok(self, request, result):
        print ("callback OK is called")
        # Enable the item
        self.isEnabled = True
        self.source = "images/play.png"
        
    def callback_fail(self,request, result):
        print('callback fail called')
        # Disable the frame
        #self.isEnabled = False
        self.source = "images/stop.png"

    def __init__(self, camera_url, **kwargs):
        super().__init__(**kwargs)
        self.camera_url = camera_url
        if not (self.t_status_checker):
           self.t_status_checker = threading.Thread(target = self.check)
           print ('Starting camera checker thread')
           self.t_status_checker.start()
        with self.canvas.before:
            self.r = random.random()
            self.g = random.random()
            self.b = random.random()
            Color(self.r,self.g,self.b)
            self.texture = Texture.create()
            self.rect = Rectangle ()
            self.bind (pos = self.update_rect, size = self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        #self.source.size = (self.width-20, self.height-20)

    def stop(self):
        self.stop_flag=True


class CameraLive(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.r = random.random()
            self.g = random.random()
            self.b = random.random()
            Color(self.r,self.g,self.b)
            self.rect = Rectangle (pos=self.pos, size = self.size)
            self.bind (pos = self.update_rect, size = self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size