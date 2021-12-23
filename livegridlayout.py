from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.core.window import Window

class LiveGridLayout(GridLayout):
    nLive = NumericProperty(0)
    #maxWidth = 0
    #maxHeight = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #     self.bind (size = self.get_max_size)

    # def get_max_size(self, *args):
    #     if (self.size [0] > self.maxWidth):
    #         self.maxWidth = self.size[0]
    #     if (self.size [1] > self.maxHeight):
    #         self.maxHeight = self.size[1]