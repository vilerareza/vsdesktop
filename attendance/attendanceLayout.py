import sqlite3
import uuid
import datetime
import cv2
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.clock import Clock

from attendance.person import PersonList

Builder.load_file('attendance/attendanceLayout.kv')

class AttendanceLayout(BoxLayout):
    db = ObjectProperty({'dbName': 'attendance/attendanceData.db', 'tableName': 'data'})
    rightBox = ObjectProperty(None)
    listData = ListProperty([])
    listName = ListProperty([])
    index = NumericProperty(2)
    personListBox = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.personListBox = PersonList()
        self.tableBox = FloatLayout()
        self.table = MDDataTable(size_hint=(0.9, 0.9),
                                #  background_color_header= [0.5, 0.5, 0.5, 0],
                                #  background_color_cell= [0.5, 0.5, 0.5, 0],
                                 pos_hint = {'center_x': 0.5, 'center_y': 0.5},
                                 column_data=[
                                    ("Id", dp(20)),
                                    ("Name", dp(40)),
                                    ("Date", dp(30)),
                                    ("Time", dp(30)),
                                    ("Room", dp(20)),
                                    ("Photo", dp(40))
                                 ],
                                 use_pagination=True,
                                 pagination_menu_height = '240dp',
                                 rows_num = 7)
        self.tableBox.add_widget(self.table)
        # self.bind(listName = self.personListBox.get_name)
        # self.get_item_from_db()

    def get_item_from_db(self):
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "SELECT * FROM "+tableName+""
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            self.listData.append(entry)
            self.listName.append(entry[1])
        con.close()

        self.table.row_data = self.listData

    def add_to_db(self, data):
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = "INSERT INTO "+tableName+" (name, date, time, room, photo)VALUES('"+data[0]+"','"+data[1]+"','"+data[2]+"','"+data[3]+"','"+data[4]+"')"
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def add_data(self, face, label):
        for i in range(len(face)):
            saveTempPath = 'images/temp/database/'
            uuidName = uuid.uuid4()
            writePath = (f'{saveTempPath}{uuidName}.png')
            print(face[i])
            cv2.imwrite(writePath, face[i])
            # id = str(self.index)
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            room = str(501)
            # photo = Image(source = 'images/cancelbutton.png')
            # photos = photo.texture
            data = label[i], date, time, room, writePath
            self.listData.append(data)
            # self.table.row_data = self.listData
            # self.index += 1
            self.add_to_db(data)
            print('Data added to database')

    def show_all(self):
        self.rightBox.clear_widgets()
        self.rightBox.add_widget(self.tableBox)

    def show_person(self):
        self.rightBox.clear_widgets()
        self.rightBox.add_widget(self.personListBox)






