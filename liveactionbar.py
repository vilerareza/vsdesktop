from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('liveactionbar.kv')

class LiveActionBar (GridLayout):
    pass

    def button_press_callback(self, button):
        button.source = 'images/capturedown.png'
        if self.parent:
            self.parent.capture_image()
        #manager = App.get_running_app().manager
    
    def button_release_callback(self, button):
        button.source = 'images/capturenormal.png'