from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class SelectionBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        # self.selectionBox = GridLayout(cols =3, size_hint= (None,None))
        # self.nextButton = Button(background_disabled_normal = 'images/right2.png',
        #                          background_down = 'images/right3.png',
        #                          size_hint = (0.2, 1))
        # self.previousButton = Button(background_disabled_normal = 'images/left2.png',
        #                              background_down = 'images/left3.png',
        #                              size_hint = (0.2, 1))
        # self.selection = GridLayout(rows =1, size_hint= (None,None))
        # self.selectionBox.add_widget(self.previousButton)
        # self.selectionBox.add_widget(self.selection)
        # self.selectionBox.add_widget(self.nextButton)


    def add_widget(self, widget):
        super().add_widget(widget)