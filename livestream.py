from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.graphics.texture import Texture
from kivy.uix.video import Video
from kivy.properties import ObjectProperty

class LiveStream(Video):

    box_width = 50
    box_height = 50
    boundingBox = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = "stop"
        self.source = ""
        self.texture = Texture.create()
        with self.canvas.after:
            Color (0,1,0)
            self.boundingBox = Line(points = [self.center_x - self.box_width/2, self.center_y + self.box_height/2, self.center_x + self.box_width/2, self.center_y + self.box_height/2,
            self.center_x + self.box_width/2, self.center_y - self.box_height/2,
            self.center_x - self.box_width/2, self.center_y - self.box_height/2,
            self.center_x - self.box_width/2, self.center_y + self.box_height/2], width = 2)
            self.bind (pos = self.update_box, size = self.update_box)

    def update_box(self, *args):
        self.boundingBox.points = [self.center_x - self.box_width/2, self.center_y + self.box_height/2, self.center_x + self.box_width/2, self.center_y + self.box_height/2,
        self.center_x + self.box_width/2, self.center_y - self.box_height/2,
        self.center_x - self.box_width/2, self.center_y - self.box_height/2,
        self.center_x - self.box_width/2, self.center_y + self.box_height/2]

    def _on_video_frame(self, *largs):
        super()._on_video_frame(*largs)
        pass


