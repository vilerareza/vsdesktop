from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel

Builder.load_file('maintabs.kv')

class MainTabs(TabbedPanel):

    multiView = ObjectProperty(None)
    settingView = ObjectProperty(None)
    tabMultiView = ObjectProperty(None)
    tabSettingView = ObjectProperty(None)
    
    def tabSettingViewPressed(self, tab):
        if tab.state == "down":
            # Stop the multiview
            self.multiView.stop()
    
    def refreshMultiView(self, tab):
        if tab.state == "down":
            # Refresh the device list
            self.multiView.get_data_from_db()
            self.multiView.start_icons()
            
    def stop(self):
        self.multiView.stop()