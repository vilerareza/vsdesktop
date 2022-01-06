import cv2
import os
import sqlite3

from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from tkinter import Tk, filedialog

from attendance.person import PersonList

Builder.load_file('attendance/addperson.kv')

class AddPerson(GridLayout):
    nameBox = ObjectProperty(None)
    positionBox = ObjectProperty(None)
    profilePictureButton = ObjectProperty(None)
    personListBox = ObjectProperty(None)
    db = ObjectProperty({'dbName': 'attendance/attendanceData.db', 'tableName': 'employee'})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.personListBox = PersonList()

    def get_profile_picture(self, widget):
        root = Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(filetypes= [("jpg files","*.jpg"), ("png files", "*.png")])
        root.destroy()
        if filename:
            self.profilePictureButton.text = filename

    def add_person(self, widget):
        path = 'images/temp/profile/'
        name = self.nameBox.text
        position = self.positionBox.text
        img = cv2.imread(self.profilePictureButton.text)
        profile_picture_path = os.path.join(path, f'{name}.jpg')
        cv2.imwrite(profile_picture_path, img)

        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = f"INSERT INTO {tableName} (name, position, picture) VALUES ('{name}', '{position}', '{profile_picture_path}')"
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

        self.nameBox.text = ""
        self.positionBox.text = ""
        self.profilePictureButton.text = 'Add Profile Picture'

        print("Person Added!")
        self.personListBox.get_profile_database()
    

