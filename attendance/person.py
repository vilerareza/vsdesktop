import os
import sqlite3

from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from functools import partial

from attendance.calendar import CalendarBox
from attendance.summaryPerson import SummaryPersonBox

Builder.load_file('attendance/person.kv')

class PersonList(BoxLayout):
    personListLayout = ObjectProperty(None)
    listName = ListProperty([])
    dropPerson = ObjectProperty(None)
    dropPersonBox = ObjectProperty(None)
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
    listPerson = {}
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calendarBox = CalendarBox()
        self.summaryPersonBox = SummaryPersonBox()
        self.profileCardBox.clear_widgets()
        self.bind(name = self.summaryPersonBox.get_name)
        self.bind(name = self.calendarBox.get_name)
        self.get_profile_database()
        # self.bind(self.chooseButton.on_text = self.coba)

    # def get_all_person(self, attendanceLayout, listPerson):
    #     print('yoooy')
    #     self.listPerson = listPerson


    def get_profile_database(self):
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT name, position FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            self.listPerson[entry[0]] = entry[1]

        print(self.listPerson)
        con.close()   

    def drop_name(self):
        self.listName = list(self.listPerson.keys())
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
        position = self.listPerson[name]
        print(position)
        path = f"images/temp/profile/{name}.jpg"
        print(f'path = {path}')
        if os.path.exists(path):
            self.profilePicture.pict = path
        else:
            self.profilePicture.pict = 'images/temp/profile/User.png'
       
        self.nameLabel.text = name
        self.jobLabel.text = position

    def show_profile(self, widget):
        self.refresh_search_person()
        self.chooseButton.text = ""
        self.dropPerson.size = (270, 0)
        print(f'name {widget}')
        self.name = widget
        self.get_profile(self.name)
        self.summaryPersonBox.show_summary_person()
        self.calendarBox.show_calendar('change')

        if len(self.profileCardBox.children) == 0 or len(self.summaryBox.children) == 0 or len(self.bottomBox.children) == 0:
            self.profileCardBox.add_widget(self.profileCard)
            self.summaryBox.add_widget(self.summaryPersonBox)
            self.bottomBox.add_widget(self.calendarBox)

    def refresh_search_person(self):
        self.dropPerson.data.clear()
        self.dropPerson.refresh_from_data()
        self.dropPerson.refresh_from_layout()

    def search_person(self, widget):
        self.dropPerson.size = (270, 180)
        print(f'widget text {widget.text}')
        self.refresh_search_person()
        for name in self.listPerson:
            if widget.text.lower() in name.lower():
                self.dropPerson.data.append({
                    "text" : name,
                    "on_press" : partial(self.show_profile, name)
                })

        


    