from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

class StreamBox(BoxLayout):
    pass

class StreamGrid(GridLayout):
    nLive = NumericProperty(0)