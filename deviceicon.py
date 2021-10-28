import random
import threading
from functools import partial
from threading import Condition
from kivy.network.urlrequest import UrlRequest
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

from deviceiconimage import IconImage

class DeviceIcon(FloatLayout):
    statusImage = ObjectProperty(None)
    deviceName = StringProperty("")
    deviceUrl = StringProperty("")
    deviceLabel = ObjectProperty(None)
    isEnabled = BooleanProperty(True)
    t_status_checker = None
    condition = Condition()
    request_param_check = "?check"
    request_param_start = "?start"
    request_param_stop = "?stop"
    stop_flag = False
    source1 = "http://192.168.0.100:8000/"

    def __init__(self, deviceName, deviceUrl, **kwargs):
        super().__init__(**kwargs)
        self.deviceName = deviceName
        self.deviceUrl = deviceUrl
        self.statusImage = IconImage(deviceName = self.deviceName, deviceUrl = self.deviceUrl)
        self.statusImage.source = "images/connecting.png"
        self.deviceLabel = Label(text = "", font_size = 18, font_family = "arial", halign = 'center', valign = 'middle', size_hint = (None, None), size = (120,40), pos_hint = {'center_x':0.5, 'center_y': 0.5}, markup = True)
        #Add widgets
        self.add_widget(self.statusImage)
        self.add_widget(self.deviceLabel)
    #     with self.canvas.before:
    #         self.r = random.random()
    #         self.g = random.random()
    #         self.b = random.random()
    #         Color(self.r,self.g,self.b)
    #         self.rect = Rectangle (pos=self.pos, size = self.size)
    #         self.bind (pos = self.update_rect, size = self.update_rect)

    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size

    def start_status_checker(self):
        #Start the status checker thread
        if not (self.t_status_checker):
           self.t_status_checker = threading.Thread(target = self.check)
           print ('Starting device checker thread')
           self.t_status_checker.start()

    def check_camera(self):
        print ('check device')
        req = UrlRequest(url=(self.deviceUrl+self.request_param_check), on_success = self.callback_ok, timeout=2, on_error = self.callback_fail, on_failure = self.callback_fail)
        #req = UrlRequest(url=(self.source1+self.request_param_check), on_success = self.callback_ok, timeout=2, on_error = self.callback_fail, on_failure = self.callback_fail)
        
    def check(self):
        while (not self.stop_flag):
            # if the application exit then break the loop
            with self.condition:
                if not (self.condition.wait(timeout = 2)):
                    # Timeout. No frame detected
                    self.check_camera()
        # Stop the thread
        if (self.t_status_checker):
            #self.t_status_checker.join (timeout = 0.5)
            self.t_status_checker = None

    def callback_ok(self, request, result):
        print ("callback OK is called")
        # Enable the item
        self.isEnabled = True
        self.statusImage.source = "images/play3.png"
        self.deviceLabel.text = "[color=cccccc]"+self.deviceName+"[/color]"
        
    def callback_fail(self,request, result):
        print('callback fail called')
        # Disable the frame
        #self.isEnabled = False
        #self.statusImage.source = "images/play.png"
        self.statusImage.source = "images/stop2.png"
        self.deviceLabel.text = "[color=777777]"+self.deviceName+"[/color]"

    def stop(self):
        self.stop_flag=True
