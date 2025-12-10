from globals import Globals

from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.graphics import Line
from kivy.graphics import BoxShadow

class CardPlay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 20

        self.size = Globals.windowSize
        with self.canvas:
            Rectangle(source='res/texture/bg1.png', size=self.size)

        header = GridLayout(size_hint=(1,.15), cols=2, rows=1)
        header.add_widget(Button(text='<-', color=(0,0,0,1), font_size=30, halign='center', valign='center', size_hint=(.2, 1), background_color=(0,0,0,0)))
        header.add_widget(Button(text='Blablabla', color=(0,0,0,1), font_size=30, halign='center', valign='center', background_color=(0,0,0,0)))
        self.add_widget(header)

        score = BoxLayout(orientation='horizontal',size_hint=(.3, .05), pos_hint={'center_x':.5})
        score.add_widget(Label(text='3', color=(0,0,1,1), font_size=25, halign='center', valign='center'))
        score.add_widget(Label(text='1', color=(1,0,0,1), font_size=25, halign='center', valign='center'))
        score.add_widget(Label(text='2', color=(0,1,0,1), font_size=25, halign='center', valign='center'))
        self.add_widget(score)

        main = BoxLayout(orientation='vertical', size_hint=(.8, 1), pos_hint={'center_x':.5}, padding=(20,0,20,80), spacing=10)
        layout = RelativeLayout(size_hint=(1,1))
        flipArea = Button(background_color=(0,0,0,0), size_hint=(1,1), on_press=self.flipCard)
        self.cardFlipped = False
        card = BoxLayout(orientation='vertical', padding=30, size_hint=(1,1))
        with card.canvas:
            Color(0,0,0,.15)
            self.rect6 = BoxShadow(card.size, card.pos, offset=(0,-4), blur_radius=4.0)
            self.rect6.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            self.rect2 = Line(rounded_rectangle=(card.pos[0],card.pos[1],card.size[0],card.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            self.rect1 = RoundedRectangle(size=card.size, radius=(30,30,30,30))
        card.bind(size=self.updateMainCardBackGround)
        card.image = Image(source='res/texture/img1.png', fit_mode='contain')
        card.add_widget(card.image)
        card.label = Label(text='Blablabla1111', font_size=25, halign='center', valign='center', size_hint=(1, .2))
        card.add_widget(card.label)
        rate = GridLayout(cols=4, rows=1, size_hint=(1, .12), disabled=True, opacity=0)
        with rate.canvas:
            Color(0,0,0,.15)
            self.rect7 = BoxShadow(size=rate.size, pos=rate.pos, offset=(0,-4), blur_radius=4.0)
            self.rect7.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            self.rect4 = Line(rounded_rectangle=(rate.pos[0], rate.pos[1], rate.size[0], rate.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            self.rect3 = RoundedRectangle(size=rate.size, radius=(30,30,30,30))
            rate.bind(size=self.updateMainRateBackGround)
        rate.add_widget(Button(text='Again', font_size=20, halign='center', valign='center', background_color=(0,0,0,0)))
        rate.add_widget(Button(text='Hard', font_size=20, halign='center', valign='center', background_color=(0,0,0,0)))
        rate.add_widget(Button(text='Good', font_size=20, halign='center', valign='center', background_color=(0,0,0,0)))
        rate.add_widget(Button(text='Easy', font_size=20, halign='center', valign='center', background_color=(0,0,0,0)))
        layout.add_widget(flipArea)
        layout.add_widget(card)
        main.add_widget(layout)
        main.add_widget(rate)
        layout.flipArea = flipArea
        layout.card = card
        main.layout = layout
        main.rate = rate
        self.main = main
        self.add_widget(main)
        tab = Label(text='Next', font_size=22, size_hint=(1, .15), color=(1,1,1,1))
        with tab.canvas.before:
            Color(.07,.07,.07,.8)
            self.rect5=RoundedRectangle(size=tab.size, radius=(30,30,0,0))
            tab.bind(size=self.updateTabBackground)
            tab.bind(pos=self.updateTabBackground)
        self.add_widget(tab)

    def flipCard(instance, value):
        instance.showEndPlay()
        # if not instance.cardFlipped:
        #     instance.main.layout.card.label.text = 'Yohohohoh'
        #     instance.main.layout.card.image.source = 'res/texture/img2.png'
        #     instance.main.rate.disabled = False
        #     instance.main.rate.opacity = 1
        # else:
        #     instance.main.layout.card.label.text = 'Blablabla'
        #     instance.main.layout.card.image.source = 'res/texture/img1.png'
        #     instance.main.rate.disabled = True
        #     instance.main.rate.opacity = 0

        instance.cardFlipped = not instance.cardFlipped

    def showEndPlay(instance):
        instance.main.layout.card.label.text = 'Yeay!'
        instance.main.layout.card.label.font_size = 30
        instance.main.layout.card.padding = (30, 200)
        instance.main.layout.card.add_widget(Label(text='Thats\'s all for today!', font_size=25, halign='center', valign='center', size_hint=(1, .2)))
        instance.main.layout.card.remove_widget(instance.main.layout.card.image)
        instance.main.layout.card.image = None

    def updateMainCardBackGround(self, instance, value):
        self.rect1.size = instance.size
        self.rect1.pos = instance.pos
        self.rect2.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 30)
        self.rect6.size = instance.size
        self.rect6.pos = instance.pos
        self.main.layout.flipArea.size = instance.size
        self.main.layout.flipArea.pos = instance.pos

    def updateMainRateBackGround(self, instance, value):
        self.rect3.size = instance.size
        self.rect3.pos = instance.pos
        self.rect4.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 30)
        self.rect7.size = instance.size
        self.rect7.pos = instance.pos

    def updateTabBackground(self, instance, value):
        self.rect5.size = instance.size
        self.rect5.pos = instance.pos