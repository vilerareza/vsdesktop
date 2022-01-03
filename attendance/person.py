import os
import sqlite3

from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button

from attendance.calendar import CalendarBox
from attendance.summaryPerson import SummaryPersonBox

Builder.load_file('attendance/person.kv')

class PersonList(BoxLayout):
    personListLayout = ObjectProperty(None)
    listName = ListProperty([])
    dropPerson = ObjectProperty(None)
    chooseButton = ObjectProperty(None)
    attendStatus = ObjectProperty(None)
    profileCardBox = ObjectProperty(None)
    profileCard = ObjectProperty(None)
    profilePicture = ObjectProperty(None)
    nameLabel = ObjectProperty(None)
    jobLabel = ObjectProperty(None)
    bottomBox = ObjectProperty(None)
    summaryBox = ObjectProperty(None)
    calendarBox = ObjectProperty(None)
    summaryPersonBox = ObjectProperty(None)
    name = ObjectProperty(None)
    db = ObjectProperty({'dbName': 'attendance/attendanceData.db', 'tableName': 'employee'})
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calendarBox = CalendarBox()
        self.summaryPersonBox = SummaryPersonBox()
        self.profileCardBox.clear_widgets()
        self.get_profile_database()
        self.bind(name = self.summaryPersonBox.get_name)
        self.bind(name = self.calendarBox.get_name)

        # self.con = sqlite3.connect(self.db['dbName'])
        # self.cur = self.con.cursor


    def get_profile_database(self):
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT name FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            self.listName.append(entry[0])
        con.close()
    
    def get_profile_position(self, name):
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = f"SELECT position FROM {tableName} WHERE name = '{name}'"
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            position = entry[0]
        con.close()
        return position      

    def drop_name(self):
        self.listName = set(self.listName)
        print(self.listName)
        self.dropPerson.clear_widgets()
        for name in self.listName:
            personButton = Button(text = name,
                                  size_hint = (None, None),
                                  width = 150,
                                  height = 40,
                                  background_color = [0.9, 1, 0.5, 0.5])
            personButton.bind(on_release=lambda personButton: self.dropPerson.select(personButton.text))
            personButton.bind(on_press = self.show_profile)
            self.dropPerson.add_widget(personButton)
        self.dropPerson.bind(on_select=lambda instance, x: setattr(self.chooseButton, 'text', x))

    def get_profile(self, name):
        position = self.get_profile_position(name)
        print(position)
        path = f'images/temp/profile/{name}.jpg'
        if os.path.exists(path):
            self.profilePicture.pict =  path
        else:
            self.profilePicture.pict = 'images/temp/profile/User.png'
       
        self.nameLabel.text = name
        self.jobLabel.text = position

    def show_profile(self, widget):
        # self.calendarBox.refresh()
        self.name = widget.text
        self.get_profile(self.name)
        self.summaryPersonBox.show_summary_person()
        self.calendarBox.show_calendar('change')

        if len(self.profileCardBox.children) == 0 or len(self.summaryBox.children) == 0 or len(self.bottomBox.children) == 0:
            self.profileCardBox.add_widget(self.profileCard)
            self.summaryBox.add_widget(self.summaryPersonBox)
            self.bottomBox.add_widget(self.calendarBox)

        


    