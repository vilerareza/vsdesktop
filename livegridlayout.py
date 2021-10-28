from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

class LiveGridLayout(GridLayout):
    nLive = NumericProperty(0)