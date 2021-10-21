import random
from kivy.graphics import Color, Rectangle
from kivy.uix.video import Video

class StreamItem(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #     with self.canvas:
    #         self.r = random.random()
    #         self.g = random.random()
    #         self.b = random.random()
    #         Color(self.r,self.g,self.b)
    #         self.rect = Rectangle (pos=self.pos, size = self.size)
    #         self.bind (pos = self.update_rect, size = self.update_rect)
    
    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size