from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget



class Coba(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = BoxLayout(orientation = 'vertical')
        self.btn1 = Button(text = 'hello')
        self.nextButton = Button(background_disabled_normal = 'images/left2.png',
                                 background_down = 'images/left.png',
                                 background_color = [1,1,0.7,0.9])
        self.grid.add_widget(self.btn1)
        self.grid.add_widget(self.nextButton)

    def on_press(self):
        self.nextButton = 'images/left2.png'

    def on_release(self):
        self.nextButton = 'images/right2.png'


class SampleApp(App):
    def build(self):
        return Coba()


SampleApp().run()