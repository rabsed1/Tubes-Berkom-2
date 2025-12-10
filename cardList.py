from globals import Globals

from deck import Deck

from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.graphics import BoxShadow

class CardList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation='vertical'

        self.size = Globals.windowSize
        # with self.canvas:
        #     Rectangle(source='res/texture/bg1.png', size=self.size, pos=self.pos)

        header = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        header.add_widget(Button(text='<-', color=(0,0,0,1), font_size=30, halign='center', valign='center', size_hint=(.2, 1), background_color=(0,0,0,0)))
        header.add_widget(Button(text='Blablabla', color=(0,0,0,1), font_size=30, halign='center', valign='center', background_color=(0,0,0,0)))
        self.add_widget(header)
        
        main = RelativeLayout() 
        main.label = Label(text='This deck is empty...', color=(0,0,0,1), pos_hint={'center_x':.5,'center_y':.5})
        main.cardList = BoxLayout(orientation='vertical', spacing=30, padding=(0,30,0,0), size_hint=(.7, None), pos_hint={'center_x':.5, 'top':1})
        main.cardList.bind(minimum_height=self.updateCardList)
        main.cardList.arr = []
        main.add_widget(main.cardList)
        self.add_widget(main)
        self.main = main

        self.tab = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        with self.tab.canvas:
            Color(.07,.07,.07,.95)
            self.tab.rect1=RoundedRectangle(size=self.tab.size, radius=(30,30,0,0))
            self.tab.bind(size=self.updateTabBackground)
            self.tab.bind(pos=self.updateTabBackground)
        self.tab.add_widget(Button(text='Play', font_size=25, halign='center', valign='center', background_color=(0,0,0,0)))
        self.tab.add_widget(Button(text='AddCard', on_press=self.addCard, font_size=25, halign='center', valign='center', background_color=(0,0,0,0)))
        self.tab.add_widget(Button(text='Save', font_size=25, halign='center', valign='center', background_color=(0,0,0,0)))
        self.add_widget(self.tab)

        self.selectedCard = None

    def updateTabBackground(self, instance, value):
        self.tab.rect1.size = instance.size
        self.tab.rect1.pos = instance.pos

    def updateCardList(self, instance, value):
        instance.size[1] = instance.minimum_height

    def addCard(instance, value):
        card = RelativeLayout(size_hint=(1,None), size=(0,200))
        card.card1 = Deck(disabled=False, opacity=1)

        card2 = BoxLayout(orientation='vertical', padding=30, size_hint=(0,0), height=600, disabled=True, opacity=0)
        with card2.canvas:
            Color(0,0,0,.15)
            card2.rect6 = BoxShadow(card2.size, card2.pos, offset=(0,-4), blur_radius=4.0)
            card2.rect6.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            card2.rect2 = Line(rounded_rectangle=(card2.pos[0],card2.pos[1],card2.size[0],card2.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            card2.rect1 = RoundedRectangle(size=card2.size, radius=(30,30,30,30))
        card2.bind(size=instance.updateCard2Background)
        card2.header = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        card2.header.button = Button(size_hint=(.2, 1), pos_hint={'right':1}, on_press=(instance.closeEditCard))
        card2.header.add_widget(card2.header.button)
        card2.add_widget(card2.header)

        card2.image = Image(source='res/texture/img1.png', fit_mode='contain')
        card2.add_widget(card2.image)
        card2.label = Label(text='Blablabla1111', font_size=25, halign='center', valign='center', size_hint=(1, .2))
        card2.add_widget(card2.label)
        
        card.card2 = card2
        card.add_widget(card.card2)
        card.add_widget(card.card1)
        card.card1.id = len(instance.main.cardList.arr)
        instance.main.cardList.arr.append(card)
        instance.main.cardList.add_widget(card)
        card.card1.bind(on_press=instance.editCard)

    def editCard(self, instance):
        if self.selectedCard:
            self.selectedCard.card1.disabled = False
            self.selectedCard.card1.opacity = 1
            self.selectedCard.card1.size_hint=(1,None)
            self.selectedCard.card2.disabled = True
            self.selectedCard.card2.opacity = 0
            self.selectedCard.card2.size_hint=(0,0)
            self.selectedCard.card2.size=(0,0)
            self.selectedCard.size=(0, 200)
        self.selectedCard = self.main.cardList.arr[instance.id]
        self.selectedCard.card1.disabled = True
        self.selectedCard.card1.opacity = 0
        self.selectedCard.card1.size_hint=(0,0)
        self.selectedCard.card2.disabled = False
        self.selectedCard.card2.opacity = 1
        self.selectedCard.card2.size_hint=(1,None)
        self.selectedCard.card2.size=(0,600)
        self.selectedCard.size=(0, 600)

    def closeEditCard(self, instance):
        self.selectedCard.card1.disabled = False
        self.selectedCard.card1.opacity = 1
        self.selectedCard.card1.size_hint=(1,None)
        self.selectedCard.card2.disabled = True
        self.selectedCard.card2.opacity = 0
        self.selectedCard.card2.size_hint=(0,0)
        self.selectedCard.card2.size=(0,0)
        self.selectedCard.size=(0, 200)
        self.selectedCard = None

    def updateCard2Background():
        card2.rect6.pos = card2.pos
        card2.rect6.size = card2.size
