import datetime
import sqlite3

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput

Builder.load_file('attendance/summaryPerson.kv')

class SummaryPersonBox(GridLayout):
    db = ObjectProperty({'dbName': 'attendance/attendanceData.db', 'tableName': 'data'})
    name = ObjectProperty(None)
    checkinTime = ObjectProperty(None)
    checkoutTime = ObjectProperty(None)
    avgCheckinTime = ObjectProperty(None)
    avgCheckoutTime = ObjectProperty(None)
    avgWorkingTime = ObjectProperty(None)
    labelProfile = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_name(self, personList, name):
        self.name = name
        self.labelProfile.text = f"{self.name}'s Attendance Dashboard"
        
    def get_today_data(self, name, condition, textLayout):
        # today = datetime.datetime.now()
        # date = today.strftime('%Y-%m-%d')
        date = '2021-12-31'
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        if len(condition[0]) > 1:
            sql = f"SELECT min(time) FROM {tableName} WHERE name = '{name}' and date = '{date}' and (status = '{condition[0]}' or status = '{condition[1]}')"
        else:
            sql = f"SELECT min(time) FROM {tableName} WHERE name = '{name}' and date = '{date}' and status = '{condition}'"
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            time = entry[0]
        con.close()
        if time == None:
            textLayout.text = '-'
        else:
            textLayout.text = str(time)

    def get_average_data(self, name, condition, textLayout):
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        if len(condition[0]) > 1:
            sql = f"select time(avg(strftime('%s', time)), 'unixepoch') from {tableName} where time in (select min(time) from {tableName} where name = '{name}' and (status = '{condition[0]}' or status = '{condition[1]}') group by status)"
        else:
            sql = f"select time(avg(strftime('%s', time)), 'unixepoch') from {tableName} where time in (select min(time) from {tableName} where name = '{name}' and status = '{condition}')"
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            time = entry[0]
        con.close()
        if time == None:
            textLayout.text = '-'
        else:
            textLayout.text = str(time)
        
        return time

    def get_average_working(self, avgIn, avgOut):
        try:
            work = datetime.datetime.strptime(avgOut, '%H:%M:%S') - datetime.datetime.strptime(avgIn, '%H:%M:%S')
            # work = datetime.datetime.strftime(work, '%H:%M:%S')
            self.avgWorkingTime.text = str(work)
        except:
            self.avgWorkingTime.text = '-'

    def show_summary_person(self):
        self.get_today_data(self.name, ('in', 'late'), self.checkinTime)
        self.get_today_data(self.name, 'out', self.checkoutTime)
        avgIn = self.get_average_data(self.name, ('in', 'late'), self.avgCheckinTime)
        avgOut = self.get_average_data(self.name, 'out', self.avgCheckoutTime)
        self.get_average_working(avgIn, avgOut)
