from kivy.uix.gridlayout import GridLayout

class SelectionBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        #self.orientation = "horizontal"
    #     with self.canvas.before:
    #         self.r = random.random()
    #         self.g = random.random()
    #         self.b = random.random()
    #         Color(self.r,self.g,self.b)
    #         self.rect = Rectangle (pos=self.pos, size = self.size)
    #         self.bind (pos = self.update_rect, size = self.update_rect)

    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size
    #     pass

    def add_widget(self, widget):
        super().add_widget(widget)