from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from streamlayout import StreamBox, StreamGrid
from streamitem import StreamItem
from multiselectionbox import MultiSelectionBox
from multi_selection_item_image import ItemImage
from multi_selection_container import ItemContainer

import sqlite3

#Builder.load_file("multiview_test7.kv")

class Multiview(BoxLayout):

    testUrl = "images/test.mp4"

    db = ObjectProperty({'dbName': 'test.db', 'tableName': 'camera'})
    # Layout boxes
    streamBox = ObjectProperty(None)
    streamGrid = ObjectProperty(None)
    multiSelectionBox = ObjectProperty(None)
    # Object lists
    itemImages = ListProperty([])
    streams = ListProperty([])
    itemContainers = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        # Stream box (empty)
        self.streamBox = StreamBox(orientation="horizontal")
        self.streamGrid = StreamGrid(rows=1)
        self.streamBox.add_widget(self.streamGrid)
        self.add_widget(self.streamBox)
        # Selection box (empty)
        self.multiSelectionBox = MultiSelectionBox(orientation="horizontal",  size_hint = (1, None), height = 50, spacing = 15, padding = [0])
        self.add_widget(self.multiSelectionBox)
        # Get devices
        self.get_items_from_db()

    def add_live_item(self, widget, touch):
        if widget.collide_point(*touch.pos):
            if widget.isEnabled:
                if self.streams[self.itemContainers.index(widget)].state is not "play":
                    #v2=Video(source=widget.camera_url+"?start")
                    #self.streams[self.itemImages.index(widget)] =Video(source=widget.camera_url)
                    self.streams[self.itemContainers.index(widget)].source = widget.deviceUrl
                    #self.v2.bind(on_touch_down=self.remove_live_item)
                    self.streamGrid.nLive +=1
                    nLiveMax = self.streamGrid.rows**2 + self.streamGrid.rows
                    # Add row to grid item if already reach maximum item
                    if self.streamGrid.nLive > nLiveMax:
                        self.streamGrid.rows +=1
                    self.streamGrid.add_widget(self.streams[self.itemContainers.index(widget)])
                    self.streams[self.itemContainers.index(widget)].reload()
                    self.streams[self.itemContainers.index(widget)].state = "play" 
                else:
                    self.remove_live_item(widget)

    def remove_live_item(self, widget):
        # Remove widget
        self.streams[self.itemContainers.index(widget)].state = "stop"
        self.streamGrid.remove_widget(self.streams[self.itemContainers.index(widget)])
        self.streamGrid.nLive -=1
        nLiveMin = (self.streamGrid.rows-1)**2 + (self.streamGrid.rows-1)
        if self.streamGrid.nLive <= nLiveMin:
                self.streamGrid.rows -=1
                print(self.streamGrid.nLive)
                print (nLiveMin)
        print(self.streamGrid.nLive) 

    def stop_threads(self):
        for container in self.itemContainers:
            container.stop()

    def stop(self):
        # Stop videos
        for stream in self.streams:
            stream.state = "stop"
        # Clearing widgets
        self.streamGrid.clear_widgets()
        self.streamGrid.nLive = 0
        self.streamGrid.rows = 1
        # Stop threads
        self.stop_threads()

    def get_items_from_db(self):
        # Clearing previous list if any
        if len(self.itemContainers) > 0:
            self.stop_threads()
            self.itemContainers.clear()
            self.multiSelectionBox.clear_widgets()
        # Clearing widgets
        #self.streams.clear()
        # Connect to database
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT * FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        # Get stream and selection items
        for entry in cur:
            deviceID = entry [0]
            deviceName = entry[1]
            deviceUrl = entry [2]
            # Fill item container
            self.itemContainers.append(ItemContainer(deviceName = deviceName, deviceUrl = self.testUrl, size_hint = (None, 1), width = 185))
            # stream item
            self.streams.append(StreamItem())
        con.close()
        # Binding container touch down event to function and display the container
        for container in self.itemContainers:
            container.bind(on_touch_down=self.add_live_item)
            self.multiSelectionBox.add_widget(container)
            