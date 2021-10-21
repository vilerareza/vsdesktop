import random
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.graphics import Color, Rectangle

from settingview import SettingView
from multiview import Multiview

    
class Manager(BoxLayout):

    tabs = ObjectProperty
    
    orientation = "vertical"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Logo bar
        self.logoBar = LogoBar(size_hint = (1, None), height = 30)
        # Adding image, original size is 300x78
        self.logoBar.add_widget(Image(source = "images/vs_logo2.png", pos_hint = {'left': 1, 'top': 1}, size_hint = (None, 1), width = 130))
        self.add_widget(self.logoBar)
        # Adding Tabs Panel
        self.tabs = VsDesktopTabs()
        self.add_widget(self.tabs)
    
    def stop(self):
        self.tabs.stop()

class VsDesktopTabs(TabbedPanel):
    multiView = ObjectProperty()
    settingView = ObjectProperty()
    tabMultiView = ObjectProperty()
    tabSettingView = ObjectProperty()

    do_default_tab = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiView = Multiview()
        self.settingView = SettingView()
        self.tabSettingView = TabbedPanelItem(content = self.settingView, text = "Settings")
        self.tabMultiView = TabbedPanelItem(content = self.multiView, text = "Multiview")
        self.add_widget(self.tabSettingView)
        self.add_widget(self.tabMultiView)
        self.tabSettingView.bind(on_press=self.tabSettingViewPressed)
        self.tabMultiView.bind(on_press=self.refreshMultiView)
    
    def tabSettingViewPressed(self, tab):
        if tab.state == "down":
            # Stop the multiview
            self.multiView.stop()
    
    def refreshMultiView(self, tab):
        if tab.state == "down":
            # Refresh the device list
            self.multiView.get_items_from_db()
            
    def stop(self):
        self.multiView.stop_threads()

class LogoBar (FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)