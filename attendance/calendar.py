import calendar
import sqlite3
import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput


Builder.load_file('attendance/calendar.kv')

class CalendarBox(BoxLayout):
    db = ObjectProperty({'dbName': 'attendance/attendanceData.db', 'tableName': 'data'})
    name = ObjectProperty(None)
    today = ObjectProperty(None)
    year = ObjectProperty(None)
    month = ObjectProperty(None)
    months = ListProperty([])
    calendarGrid = ObjectProperty(None)
    monthText = ObjectProperty(None)
    yearText = ObjectProperty(None)
    dayGrid = ObjectProperty(None)
    activityDate = ObjectProperty(None)
    


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        today = datetime.datetime.now()
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        # self.year =  int(today.strftime('%Y'))
        # self.month = int(today.strftime('%m'))
        self.year = int('2021')
        self.month = int('12')
        self.today = f"-{self.months[self.month - 1]}, {today.strftime('%d')} {self.year}-"
        self.activityDate.text = self.today

    def get_name(self, personList, name):
        self.name = name

    def get_working_day(self, name):
        workingDay = []
        dbName = self.db['dbName']
        tableName = self.db['tableName']
        sql = f"SELECT DISTINCT date FROM {tableName} WHERE name = '{name}'"
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        cur.execute(sql)
        for entry in cur:
            date = datetime.datetime.strptime(entry[0], '%Y-%m-%d')
            date = datetime.datetime.date(date)
            workingDay.append(date)
        con.close()
        print(f'working day {workingDay}')
        return workingDay


    def create_day(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in range(len(days)):
            text = TextInput(text = days[i],
                             font_size= 16,
                             padding_y= (10, 1),
                             halign = 'center',
                             foreground_color = [1,1,1,1],
                             background_color = [0.5, 0.5, 0.5],
                             background_normal = 'attendance/images/background.png',
                             background_active = 'attendance/images/background.png',
                             readonly = True)
            self.dayGrid.add_widget(text)

    def create_date(self, year, month, workingDay):
        text = calendar.Calendar()
        dates = text.monthdatescalendar(year, month)
        self.monthText.text = self.months[(month - 1)]
        self.yearText.text = str(year)
        date_row = []
        row = len(dates)
        column = len(dates[0])
        self.calendarGrid.rows = row
        self.calendarGrid.cols = column
        print(len(dates))
        for week in dates:
            date_column = []
            for date in week:
                day = date.strftime('%d')
                date_column.append(day)
                if date.month != month:
                    dayButton = Button(text = day, color = [1, 1, 1, 0.3], disabled =  True)
                    self.calendarGrid.add_widget(dayButton)
                else:
                    if date in workingDay:
                        dayButton = Button(text = day, color = [0, 0, 0, 0.8], background_color = [1,1,0,0.8])
                    else:
                        dayButton = Button(text = day, color = [0, 0, 0, 0.8])

                    dayButton.bind(on_release = self.show_activity)
                    self.calendarGrid.add_widget(dayButton)
                        
            date_row.append(date_column)
        
    def show_calendar(self, status):
        if status == 'change':
            self.year = int('2021')
            self.month = int('12')
            
        self.refresh()
        workingDay = self.get_working_day(self.name)
        print(workingDay)
        self.create_day()
        self.create_date(self.year, self.month, workingDay = workingDay)

    def show_activity(self, widget):
        day = widget.text
        self.activityDate.text = f'-{self.months[self.month - 1]}, {day} {self.year}-'
        print('yay')

    def refresh(self):
        self.calendarGrid.clear_widgets()
        self.dayGrid.clear_widgets()
        self.activityDate.text = self.today

    def choose_month(self, widget):
        self.calendarGrid.clear_widgets()
        self.dayGrid.clear_widgets()
        self.calendarGrid.rows = 3
        self.calendarGrid.cols = 4
        text = TextInput(text = 'Choose Month:',
                             font_size= 16,
                             padding_y= (10, 1),
                             foreground_color = [1,1,1,1],
                             background_color = [0.5, 0.5, 0.5],
                             background_normal = 'attendance/images/background.png',
                             background_active = 'attendance/images/background.png',
                             readonly = True)
        self.dayGrid.add_widget(text)
        for month in self.months:
            monthButton = Button(text = month, color = [0, 0, 0, 0.8])
            monthButton.bind(on_press = self.get_month)
            self.calendarGrid.add_widget(monthButton)
    
    def get_month(self, widget):
        self.month = self.months.index(widget.text) + 1
        self.show_calendar('no')


        