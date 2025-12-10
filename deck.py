from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.graphics import BoxShadow
from kivy.graphics import RoundedRectangle

class Deck(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint=(1,None)
        self.size=(0, 200)
        self.background_color=(0,0,0,0)
        with self.canvas:
            Color(0,0,0,.25)
            self.shadow = BoxShadow(size=self.size, pos=self.pos, offset=(0,-4), blur_radius=4.0)
            self.shadow.border_radius=(45.0,45.0,45.0,45.0)
            Color(1,0,1,.6)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=(45,45,45,45))
        self.label = Label(text='Kenapa kita hidup coba', color=(1,1,0,1), font_size=30, valign='center', halign='center', size_hint=(.8,.8), pos_hint={'center_x': .5})
        self.add_widget(self.label)
        self.bind(size=self.updateSelf)
        self.bind(pos=self.updateSelf)
    
    def updateSelf(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        self.shadow.size = instance.size
        self.shadow.pos = instance.pos
        self.label.size = instance.size
        self.label.text_size = (.8*self.label.size[0], .8*self.label.size[1])
        self.label.pos = instance.pos
