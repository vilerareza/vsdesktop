from kivy.uix.image import Image
from kivy.graphics.texture import Texture

class ItemImage(Image):
    def __init__(self, deviceName, deviceUrl, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x':0.5, 'center_y': 0.5}
        self.texture = Texture.create()