import threading
from threading import Condition
from ffpyplayer.player import MediaPlayer
from kivy.app import App, ObjectProperty
from kivy.core.video import video_ffpyplayer
from kivy.graphics import Color, Rectangle
from kivy.loader import Loader
from kivy.network.urlrequest import UrlRequest
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.video import Video

from manager import Manager

# source1 = "http://192.168.0.101:8000/"
# source2 = "http://192.168.0.101:8000/"

stop_flag = False

# class VideoCore(video_ffpyplayer.VideoFFPy):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         print("I am used")
        
#     def _callback_ref(self):
#         print("HEYYY")

class Frame1(Video):
    global source1
    global source2
    #isEnabled = BooleanProperty(True)
    isEnabled = BooleanProperty(False)
    t_status_checker = None
    condition = Condition()
    request_param_check = "?check"
    request_param_start = "?start"
    request_param_stop = "?stop"

    def check_camera(self):
        print ('check camera')
        req = UrlRequest(url=source1+self.request_param_check+self.request_param_check, on_success = self.callback_ok, timeout=2, on_error = self.callback_fail, on_failure = self.callback_fail)
        
    def check(self):
        global stop_flag
        while (not stop_flag):
            # if the application exit then break the loop
            #self.check_camera()
            with self.condition:
                if not (self.condition.wait(timeout = 2)):
                    pass
                    # Timeout. No frame detected
                    self.check_camera()

    def callback_ok(self, request, result):
        print ("callback OK is called")
        # Enable the frame
        self.isEnabled = True
        # Only update the source if the state is not playing
        if not (self.state == 'play'):
            # The state is not playing. Update the appearance and source
            # with self.canvas.before:
            #     Color(0,0,0)
            #     Rectangle(pos=self.pos, size = self.size)
            self.source = "images/play.png"
        
    def callback_fail(self,request, result):
        print('callback fail called')
        # Enable the frame
        self.isEnabled = False
        # Update the appearance and source
        # with self.canvas.before:
        #     Color(0,0,1)
        #     Rectangle(pos=self.pos, size = self.size)
        self.source = "images/stop.png"
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # with self.canvas:
        #     Color(0,0,0)
        #     Rectangle(pos=self.pos, size = self.size)
        # Start the camera status checker thread
        if not (self.t_status_checker):
           self.t_status_checker = threading.Thread(target = self.check)
           print ('Starting camera checker thread')
           self.t_status_checker.start()
        
    def _on_video_frame(self, *largs):
        super()._on_video_frame(*largs)
        with self.condition:
            # Frame exist. Notify the condition so it will not time out
            self.condition.notify_all()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('Frame1 is pressed') 
            if self.isEnabled:
                if (self.state == "stop"):
                    self.source = source1 + "?start"
                    #self.source = "images/test.mp4"
                    self.reload()
                    self.state = "play"
                    #print(self._video)
                else:
                    self.source = 'images/play.png'
                    self.reload()
                    req = UrlRequest(source1 +"?stop")
                    self.state = "stop"

class Frame2(Video):
    # global source1
    # global source2

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.state = "stop"

    # def _on_video_frame(self, *largs):
    #         super()._on_video_frame()
    #         print('frame')

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         print('Frame2 is pressed')
    #         if (self.state == "stop"):
    #             try:
    #                 pass
    #                 #self._video._ffplayer = MediaPlayer()
    #                 self.source = source1 + "?start"
    #                 #self.reload()
    #             except Exception as e:
    #                 print(e)
    #             print(self._video._ffplayer)
    #             print(self._video._player_callback)
    #             self._video._player_callback = print_test
    #             self.state = "play"
    #             #self._video = 
    #             #print(self._video._ffplayer)
                
    #             #self._video._ffplayer = MediaPlayer(filename = source1)
    #             #self._video._callback_ref()

    #         else:
    #             self.source = 'images/play.png'
    #             self.reload()
    #             req = UrlRequest(source2 +"?stop")
    #             self.state = "stop"
    global source1
    global source2
    isEnabled = BooleanProperty(False)
    t_status_checker = None
    condition = Condition()
    request_param_check = "?check"
    request_param_start = "?start"
    request_param_stop = "?stop"

    def check_camera(self):
        print ('check camera')
        req = UrlRequest(url=source2+self.request_param_check+self.request_param_check, on_success = self.callback_ok, timeout=2, on_error = self.callback_fail, on_failure = self.callback_fail)
        
    def check(self):
        global stop_flag
        while (not stop_flag):
            # if the application exit then break the loop
            with self.condition:
                if not (self.condition.wait(timeout = 2)):
                    pass
                    # Timeout. No frame detected
                    self.check_camera()

    def callback_ok(self, request, result):
        print ("callback OK is called")
        # Enable the frame
        self.isEnabled = True
        # Only update the source if the state is not playing
        if not (self.state == 'play'):
            # The state is not playing. Update the appearance and source
            # with self.canvas.before:
            #     Color(0,0,0)
            #     Rectangle(pos=self.pos, size = self.size)
            self.source = "images/play.png"
        
    def callback_fail(self,request, result):
        print('callback fail called')
        # Enable the frame
        self.isEnabled = False
        # Update the appearance and source
        # with self.canvas.before:
        #     Color(0,1,0)
        #     Rectangle(pos=self.pos, size = self.size)
        self.source = "images/stop.png"
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # with self.canvas:
        #     Color(0,0,0)
        #     Rectangle(pos=self.pos, size = self.size)
        # Start the camera status checker thread
        if not (self.t_status_checker):
           self.t_status_checker = threading.Thread(target = self.check)
           print ('Starting camera checker thread')
           self.t_status_checker.start()
        
    def _on_video_frame(self, *largs):
        super()._on_video_frame(*largs)
        with self.condition:
            # Frame exist. Notify the condition so it will not time out
            self.condition.notify_all()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('Frame1 is pressed') 
            if self.isEnabled:
                if (self.state == "stop"):
                    self.source = source2 + "?start"
                    self.reload()
                    self.state = "play"
                    #print(self._video)
                else:
                    self.source = 'images/play.png'
                    self.reload()
                    req = UrlRequest(source2 +"?stop")
                    self.state = "stop"

class VsDesktopApp(App):

    manager = ObjectProperty(None)
    stop_flag = BooleanProperty(False)

    # def build (self):
    #     self.manager = PictureBox3()
    #     return self.manager

    # def on_stop(self):
    #     global stop_flag
    #     stop_flag = True

    def build (self):
        self.manager = MainBox()
        return self.manager

    def on_stop(self):
        self.stop_flag = True
        self.manager.stop()

#class PictureBox (BoxLayout):
#    autoPlay = False

# class PictureBox2 (GridLayout):
#     autoPlay = False

# class PictureBox3 (BoxLayout):
#     autoPlay = False


VsDesktopApp().run()
