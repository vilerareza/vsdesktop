from kivy.app import App, ObjectProperty
from kivy.properties import BooleanProperty, ObjectProperty

from manager import Manager

class VsDesktopApp(App):

    manager = ObjectProperty(None)
    stop_flag = BooleanProperty(False)

    def build (self):
        self.manager = Manager()
        return self.manager

    def on_stop(self):
        self.stop_flag = True
        self.manager.stop()

VsDesktopApp().run()
