from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from livegridlayout import LiveGridLayout
from selectionbox import SelectionBox
from deviceicon import DeviceIcon
from livebox import LiveBox

import sqlite3

Builder.load_file("multiview.kv")

class Multiview(BoxLayout):

    testUrl = "images/test.mp4"

    db = ObjectProperty({'dbName': 'test.db', 'tableName': 'camera'})
    # Layout boxes #
    # Grid layout for live stream
    liveGrid = ObjectProperty(None)
    # Layout for device selection to stream
    selectionBox = ObjectProperty(None)
    # Selection scroll view
    selectionScroll = ObjectProperty(None)
    # Object lists #
    # List for live stream objects
    liveBoxes = ListProperty([])
    # List for device selection icons
    deviceIcons = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        # Stream box (empty)
        self.liveGrid = LiveGridLayout(rows=1, spacing = 15)
        self.add_widget(self.liveGrid)
        # Selection scroll 
        #self.selectionScroll = ScrollView(do_scroll_y = False, do_scroll_x = True, size_hint_y = None, height = 50, bar_width = 3,bar_pos_x = 'top', bar_color = (0.47,0.81,0.99,0.7), bar_inactive_color = (0.47,0.81,0.99,0.4), bar_margin = 0)
        self.selectionScroll = ScrollView(do_scroll_y = False, do_scroll_x = True, size_hint_y = None, height = 50, bar_width = 3,bar_pos_x = 'top', bar_color = (0.7,0.7,0.7,0.7), bar_inactive_color = (0.7,0.7,0.7,0.4), bar_margin = 0)
        # Selection box (empty)
        self.selectionBox = SelectionBox(size_hint = (None, 1), spacing = 15, padding = [0, 3, 0, 0])
        self.selectionScroll.add_widget(self.selectionBox)
        self.add_widget(self.selectionScroll)
        # Get devices
        self.get_items_from_db()

    def add_live_box(self, deviceIcon, touch):
        if deviceIcon.collide_point(*touch.pos):
            if deviceIcon.isEnabled:
                if self.liveBoxes[self.deviceIcons.index(deviceIcon)].status is not "play":
                    # If the live stream object status is not playing then add #
                    # Start the live steaming object
                    if (deviceIcon.deviceName == "Device 1"):
                        self.liveBoxes[self.deviceIcons.index(deviceIcon)].start_live_stream(deviceIcon.deviceUrl+"?start")                    
                    else:
                        self.liveBoxes[self.deviceIcons.index(deviceIcon)].start_live_stream(self.testUrl)
                    # Adjust live grid layout for displaying live stream #
                    self.liveGrid.nLive +=1
                    nLiveMax = self.liveGrid.rows**2 + self.liveGrid.rows
                    # Add row to grid item if already reach maximum item
                    if self.liveGrid.nLive > nLiveMax:
                        self.liveGrid.rows +=1
                    # Display the live stream object to live grid layout
                    self.liveGrid.add_widget(self.liveBoxes[self.deviceIcons.index(deviceIcon)])
                else:
                    # If the live stream object status is playing then remove
                    self.remove_live_box(deviceIcon)

    def remove_live_box(self, deviceIcon):
        # Stop live stream object
        self.liveBoxes[self.deviceIcons.index(deviceIcon)].stop_live_stream()
        # Remove live stream object from live grid layout
        self.liveGrid.remove_widget(self.liveBoxes[self.deviceIcons.index(deviceIcon)])
        # Re-adjust live grid layout
        self.liveGrid.nLive -=1
        nLiveMin = (self.liveGrid.rows-1)**2 + (self.liveGrid.rows-1)
        if self.liveGrid.nLive <= nLiveMin:
                self.liveGrid.rows -=1
                print(self.liveGrid.nLive)
                print (nLiveMin)
        print(self.liveGrid.nLive) 

    def stop_icons(self):
        for deviceIcon in self.deviceIcons:
            deviceIcon.stop()
        self.selectionBox.clear_widgets()
        self.deviceIcons.clear()

    def stop_streams(self):
        # Stop live streams anyway
        for liveBox in self.liveBoxes:
            liveBox.stop_live_stream()
        # Reset and clearing widgets from liveGrid
        self.liveGrid.clear_widgets()
        self.liveGrid.nLive = 0
        self.liveGrid.rows = 1
        # Clear the list of live stream objects
        self.liveBoxes.clear()

    def stop(self):
        self.stop_streams()
        self.stop_icons()

    def get_items_from_db(self):
        # Clearing previous device stream objects and icons if any
        if len(self.deviceIcons) > 0:
            self.stop()
        # Connect to database
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT * FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        # Get device icons and stream objects
        for entry in cur:
            deviceID = entry [0]
            deviceName = entry[1]
            deviceUrl = entry [2]
            # Fill device icon list
            self.deviceIcons.append(DeviceIcon(deviceName = deviceName, deviceUrl = deviceUrl, size_hint = (None, 1), width = 185))
            # Fill live stream object list
            self.liveBoxes.append(LiveBox())
        con.close()
        # Add the container to selection box
        for deviceIcon in self.deviceIcons:
            self.selectionBox.add_widget(deviceIcon)
    
    def start_icons(self):
        if (len(self.deviceIcons) > 0):
            for deviceIcon in self.deviceIcons:
                # Start the status checker
                deviceIcon.start_status_checker()
                # Binding the touch down event
                deviceIcon.bind(on_touch_down=self.add_live_box)

    def experiment_function(self, widget, touch):
        if widget.collide_point(*touch.pos):
            widget.texture.save("testimage.jpg")
            print ("Stream 1 TOUCHED")
