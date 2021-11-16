from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.label import Label

from mylayoutwidgets import ColorLabel
from mylayoutwidgets import ToggleButtonBinded
from mylayoutwidgets import TextInputBinded
from mylayoutwidgets import ButtonBinded

from functools import partial

class DeviceInfo(FloatLayout):

    noSelectionLabel = ObjectProperty(None)
    titleLabel = ObjectProperty(None)
    messageLabel = ObjectProperty(None)
    deviceNameLabel = ObjectProperty(None)
    deviceUrlLabel = ObjectProperty(None)
    actionButton = ObjectProperty(None)
    removeButton = ObjectProperty(None)
    deviceNameText = ObjectProperty(None)
    deviceUrlText = ObjectProperty(None)
    editMode = BooleanProperty(False)
    saveToDb = BooleanProperty(False)
    switchMode = BooleanProperty(False)
    validityMessageLabel = ObjectProperty(None)
    widget_x_offset = NumericProperty(0.25)
    dbDeviceNames = ObjectProperty(None)
    selectedDeviceName = StringProperty("")
    selectedDeviceUrl = StringProperty("")
    switchBox = ObjectProperty(None)
    switchButton = ObjectProperty(None)
    recognitionStatus = StringProperty("Stop")
   
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        # Initialize widgets
        self.noSelectionLabel = ColorLabel(text ='Select a Device...', font_size = 24, font_family = "arial", halign = 'center', valign = 'middle', pos_hint = {'center_x':0.5, 'center_y': 0.55}, size_hint = (None, None), size = (300, 40))
        self.titleLabel = ColorLabel(text ='Device Info', font_size = 30, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'x':self.widget_x_offset, 'top': 0.9}, size_hint = (None, None), size = (200, 40))
        self.deviceNameLabel = ColorLabel(text ='Name:', font_size = 20, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'x':self.widget_x_offset}, size_hint = (None, None), size = (200, 40))
        self.deviceNameText = TextInputBinded(disabled = True, text = '', font_size = 20, font_family = "arial", multiline = False, size_hint = (None,None), size = (250, 40), pos_hint = {'x':self.widget_x_offset})
        self.deviceUrlLabel = ColorLabel(text ='Url:', font_size = 20, font_family = "arial", halign = 'left', valign = 'middle', pos_hint = {'x':self.widget_x_offset}, size_hint = (None, None), size = (200, 40))
        self.deviceUrlText = TextInputBinded(disabled = True, text = '', font_size = 20, font_family = "arial", multiline = False, size_hint = (None,None), size = (250, 40), pos_hint = {'x':self.widget_x_offset})
        self.actionButton = ToggleButtonBinded (text = 'Edit', size_hint = (None, None), size = (dp(80), dp(40)))
        self.removeButton = ButtonBinded (text = 'Remove', size_hint = (None, None), size = (dp(80), dp(40)))
        self.messageLabel = ColorLabel(text ='', font_size = 16, font_family = "arial", halign = 'center', valign = 'middle', pos_hint = {'center_x':0.5}, size_hint = (None, None), size = (200, 40), markup = True)
        self.validityMessageLabel = ColorLabel(text ='Validity message label', font_size = 16, font_family = "arial", halign = 'center', valign = 'middle', pos_hint = {'center_x':0.5}, size_hint = (None, None), size = (200, 40), markup = True)
        #Switch
        self.switchBox = BoxLayout(orientation = 'horizontal', pos_hint = {'x':self.widget_x_offset}, size_hint = (None, None), size = (250, 40))
        self.switchLabel = Label(text = 'Face Recognition')
        self.switchButton = Switch(active = False)
        self.switchButton.bind(active = self.switch_click)
        self.switchBox.add_widget(self.switchLabel)
        self.switchBox.add_widget(self.switchButton)
        # Binding button press to change mode
        self.actionButton.bind(on_press = self.change_mode)
        # Position binding
        self.titleLabel.bind(y = (partial(self.deviceNameLabel.update_y_position, offset = 50)))
        self.deviceNameLabel.bind(y = (partial(self.deviceNameText.update_y_position, offset = 40)))
        self.deviceNameText.bind(y = (partial(self.deviceUrlLabel.update_y_position, offset = 50)))
        self.deviceUrlLabel.bind(y = (partial(self.deviceUrlText.update_y_position, offset = 40)))
        self.deviceUrlText.bind(y = (partial(self.actionButton.update_y_position, offset = 60)), right = self.actionButton.update_right_position)
        self.actionButton.bind(y = (partial(self.removeButton.update_y_position, offset = 70)), right = self.removeButton.align_right)
        self.noSelectionLabel.bind(y = (partial(self.messageLabel.update_y_position, offset = -40)), right = self.removeButton.align_right)
        # Go to no-selection configuration first
        self.no_selection_config()

        with self.canvas.before:
            Color(color[0],color[1],color[2])
            self.rect = Rectangle (pos=self.pos, size = self.size)
            self.bind (pos = self.update_rect, size = self.update_rect)
    
    def switch_click(self, switchObject, switchValue):
        # print(self.recognitionStatus)
        if (switchValue):
            self.recognitionStatus = 'Start'
        else:
            self.recognitionStatus = 'Stop'


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def display_info(self, deviceList, selectedDevice):
        self.selectedDeviceName = selectedDevice.deviceName
        self.selectedDeviceUrl = selectedDevice.deviceUrl
        self.titleLabel.text = "Device Info"
        self.deviceNameText.text = self.selectedDeviceName
        self.deviceUrlText.text = self.selectedDeviceUrl
        if selectedDevice.recognitionStatus == 'Stop':
            self.switchButton.active = False
        else:
            self.switchButton.active = True
        

    def change_config(self, deviceList, isDeviceSelected, message = ""):
        print (isDeviceSelected)
        if (isDeviceSelected == True):
            print ('TO DEVICE INFO')
            self.device_info_config()
        else:
            if not self.editMode:
                self.no_selection_config(message)
                print ('TO NO SELECTION')

    def no_selection_config(self, message = ""):
        # Clearing widgets
        self.clear_widgets()
        self.messageLabel.text = "[color=dddddd]"+message+"[/color]"
        self.add_widget(self.noSelectionLabel)
        self.add_widget(self.messageLabel)

    def device_info_config(self):
        # Clearing widgets
        self.clear_widgets()
        # Adding widgets
        self.add_widget(self.titleLabel)
        self.add_widget(self.deviceNameLabel)
        self.add_widget(self.deviceNameText)
        self.add_widget(self.deviceUrlLabel)
        self.add_widget(self.deviceUrlText)
        self.add_widget(self.actionButton)
        self.add_widget(self.removeButton)
        self.add_widget(self.switchBox)
        self.switchBox.disabled = True
    
    def change_mode(self, widget):
        # if self.entry_check (self.deviceNameText.text, self.deviceUrlText.text, self.get_name_from_parrent_devices()):
        # if self.entry_check (self.deviceNameText.text, self.deviceUrlText.text, self.dbDeviceNames):
        if (widget.state == 'down'):
            self.editMode = True
            widget.text = "Save"
            self.deviceNameText.disabled = False
            self.deviceUrlText.disabled = False
            self.removeButton.disabled = True
            self.switchBox.disabled = False

        else:
            if self.entry_check (self.deviceNameText.text, self.deviceUrlText.text, self.dbDeviceNames):
                # trigger to change entry in database
                print ('ENTRY CHECK OK')
                self.editMode = False
                widget.text = "Edit"
                self.deviceNameText.disabled = True
                self.deviceUrlText.disabled = True
                self.removeButton.disabled = False
                self.switchBox.disabled = True
            else:
                # Force button to stay down
                self.actionButton.state = 'down'
    
    def entry_check(self, newDeviceName, newDeviceUrl, nameList = []):
        namesToCheck = nameList.copy()
        # Check for empty entry
        if (newDeviceName == "") or (newDeviceUrl ==""):
            print ("Name or URL cannot be empty...")
            return False
        # Check for existing entry in nameList
        # Excluding currently selected device first
        for index, name in enumerate(namesToCheck):
            if name == self.selectedDeviceName:
                namesToCheck.pop(index)
        for name in namesToCheck:
            if name == newDeviceName:
                print ("Not saved, device name already exist...")
                return False

        return True

    def get_name_from_parrent_devices(self):
        names = []
        for device in self.parrentDevices:
            names.append(device.deviceName)
        return names