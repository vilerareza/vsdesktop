from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from settingview import SettingView
from multiview import Multiview
from attendance.attendanceLayout import AttendanceLayout

Builder.load_file('maintabs.kv')

class MainTabs(TabbedPanel):

    multiView = ObjectProperty(None)
    settingView = ObjectProperty(None)
    tabMultiView = ObjectProperty(None)
    tabSettingView = ObjectProperty(None)
    tabList = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiView = Multiview()
        self.settingView = SettingView()
        self.listView = AttendanceLayout()
        self.tabSettingView = TabbedPanelItem(content = self.settingView)
        self.add_widget(self.tabSettingView)
        self.tabMultiView = TabbedPanelItem(content = self.multiView)
        self.add_widget(self.tabMultiView)
        self.tabListView = TabbedPanelItem(content = self.listView)
        self.add_widget(self.tabListView)
        self.tabSettingView.bind(on_press=self.tabSettingViewPressed)
        self.tabMultiView.bind(on_press=self.refreshMultiView)
        self.tabListView.bind(on_press=self.tabListViewPressed)

    def tabSettingViewPressed(self, tab):
        if tab.state == "down":
            # Stop the multiview
            self.multiView.stop()
    
    def refreshMultiView(self, tab):
        if tab.state == "down":
            # Refresh the device list
            self.multiView.get_data_from_db()
            self.multiView.start_icons()

    def tabListViewPressed(self, tab):
        if tab.state == "down":
            # Stop the multiview
            self.listView.get_item_from_db()
            
    def stop(self):
        self.multiView.stop()