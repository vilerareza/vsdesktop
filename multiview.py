from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from deviceicon import DeviceIcon
from livebox import LiveBox
import sqlite3

Builder.load_file("multiview.kv")

class Multiview(BoxLayout):
    # Grid layout for live stream
    liveGrid = ObjectProperty(None)
    # Layout for device selection to stream
    selectionBox = ObjectProperty(None)
    # Selection scroll view
    selectionScroll = ObjectProperty(None)
    # List for live stream objects
    liveBoxes = ListProperty([])
    # List for device selection icons
    deviceIcons = ListProperty([])
    # Application manager class
    manager = ObjectProperty(None)
    # Device icon selection scroll buttons
    selectionNextButton = ObjectProperty(None)
    selectionBackButton = ObjectProperty(None)
    selectionInterval = 4

    testUrl = "images/test.mp4"

    db = ObjectProperty({'dbName': 'test.db', 'tableName': 'camera'})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print (f'TYPE GRID {type(self.liveGrid)}')
        # Get devices
        #self.get_items_from_db()
    #     Window.bind(on_resize=self.on_resize)
    
    # def on_resize(self, *args):
    #     print ('RESIZE')

    def icon_touch_action(self, deviceIcon, touch):
        if deviceIcon.collide_point(*touch.pos):
            if deviceIcon.isEnabled:
                if self.liveBoxes[self.deviceIcons.index(deviceIcon)].status != "play":
                    # If the live stream object status is not playing then add #
                    self.show_live_box(deviceIcon)
                else:
                    # If the live stream object status is playing then remove
                    self.remove_live_box(deviceIcon)
            

    def show_live_box(self, deviceIcon):
        # Start the live steaming object
        # if (deviceIcon.deviceName == "Device 1" or deviceIcon.deviceName == "Device 2"):
        #     self.liveBoxes[self.deviceIcons.index(deviceIcon)].start_live_stream(deviceIcon.deviceUrl+"?start")                    
        # else:
        self.liveBoxes[self.deviceIcons.index(deviceIcon)].start_live_stream(self.testUrl)
        # Adjust live grid row and cols for displaying live stream #
        self.liveGrid.nLive +=1
        rowLimit = self.liveGrid.rows**2 + self.liveGrid.rows
        if self.liveGrid.nLive > rowLimit:
            self.liveGrid.rows +=1
        colLimit = self.liveGrid.cols**2
        if (self.liveGrid.nLive > colLimit):
            self.liveGrid.cols +=1
        # Display the live stream object to live grid layout
        self.liveGrid.add_widget(self.liveBoxes[self.deviceIcons.index(deviceIcon)])
        # Adjust the livestream to the size of livebox
        self.adjust_livebox_size()
        print (f'ROWS : {self.liveGrid.rows} COLS : {self.liveGrid.cols}')

    def remove_live_box(self, deviceIcon):
        # Stop live stream object
        self.liveBoxes[self.deviceIcons.index(deviceIcon)].stop_live_stream()
        # Remove live stream object from live grid layout
        self.liveGrid.remove_widget(self.liveBoxes[self.deviceIcons.index(deviceIcon)])
        # Re-adjust live grid rows and cols
        self.liveGrid.nLive -=1
        if self.liveGrid.nLive > 0:
            rowLimit = (self.liveGrid.rows-1)**2 + (self.liveGrid.rows-1)
            if self.liveGrid.nLive <= rowLimit:
                self.liveGrid.rows -=1
            colLimit = (self.liveGrid.cols-1)**2
            if (self.liveGrid.nLive <= colLimit):
                self.liveGrid.cols -=1
            # Adjust the livestream to the size of livebox
            self.adjust_livebox_size()
        print (f'ROWS : {self.liveGrid.rows} COLS : {self.liveGrid.cols}')

    def adjust_livebox_size(self):
        print (f'LIVEGRID SIZE : {str(self.liveGrid.size)}')
        cell_width = int((self.liveGrid.width - self.liveGrid.spacing[0]*(self.liveGrid.cols-1))/
                    self.liveGrid.cols)
        cell_height = int((self.liveGrid.height - self.liveGrid.spacing[0]*(self.liveGrid.rows-1))/
                    self.liveGrid.rows)
        for livebox in self.liveBoxes:
            livebox.adjust_self_size(size = (cell_width, cell_height))

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
        self.liveGrid.cols = 1
        # Clear the list of live stream objects
        self.liveBoxes.clear()

    def stop(self):
        self.stop_streams()
        self.stop_icons()

    def get_data_from_db(self):
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
        self.create_deviceicon_livebox(cur)
        con.close()

    def create_deviceicon_livebox(self, db_cursor):
        for entry in db_cursor:
            deviceID = entry [0]
            deviceName = entry[1]
            deviceUrl = entry [2]
            deviceNeuralNet = entry [3]
            # Fill device icon list
            self.deviceIcons.append(DeviceIcon(deviceName = deviceName, deviceUrl = deviceUrl, size_hint = (None, None), size = (181, 45)))
            # Fill live stream object list
            if deviceNeuralNet == 1:
                if not (self.manager.model):
                    self.manager.activate_vision_ai()
                if self.manager.model:
                    self.liveBoxes.append(LiveBox(detector = self.manager.detector, model = self.manager.model, model_properties = self.manager.model_properties, 
                    dbVectors = self.manager.dbVectors, fileNames = self.manager.fileNames))
            else:
                self.liveBoxes.append(LiveBox())
        # Add deviceIcon content to selection box
        self.add_deviceicon_to_selectionbox(item_list = self.deviceIcons, container = self.selectionBox)

    def add_deviceicon_to_selectionbox(self, item_list, container):
        for item in item_list:
            container.add_widget(item)
    
    def start_icons(self):
        if (len(self.deviceIcons) > 0):
            for deviceIcon in self.deviceIcons:
                # Start the status checker
                deviceIcon.start_status_checker()
                # Binding the touch down event
                deviceIcon.bind(on_touch_down=self.icon_touch_action)
  
    def selection_next_press(self, button):
        if self.selectionScroll.scroll_x < 1:
            self.selectionScroll.scroll_x += 0.1
            if self.selectionScroll.scroll_x >= 1:
                self.selectionScroll.scroll_x = 1

    def selection_back_press(self, button):
        if self.selectionScroll.scroll_x > 0:
            self.selectionScroll.scroll_x -= 0.1
            if self.selectionScroll.scroll_x <= 0:
                self.selectionScroll.scroll_x = 0