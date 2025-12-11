from globals import Globals

from deck import Deck

from kivy.app import App

from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooser
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.graphics import BoxShadow
from kivy.graphics import Line

class CardList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation='vertical'
        self.size = Globals.windowSize

        self.selectedCard = None

        with self.canvas:
            Rectangle(source='res/textures/bg1.png', size=self.size, pos=self.pos)

        header = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        header.add_widget(Button(text='<-', color=(0,0,0,1), font_name='Jersey10', font_size=34, halign='center', valign='center', size_hint=(.2, 1), background_color=(0,0,0,0), on_press=self.toDeckList))
        title = Button(text='Blablabla', color=(0,0,0,1), font_name='Jersey10', font_size=34, halign='left', valign='center', background_color=(0,0,0,0))
        title.bind(size=self.updateTitleSizePos)
        header.add_widget(title)
        header.title = title
        self.add_widget(header)
        
        main = ScrollView(pos_hint={'center_x':.5}) 
        main.label = Label(text='This deck is empty...', color=(0,0,0,1), pos_hint={'center_x':.5,'center_y':.5})
        main.cardList = BoxLayout(orientation='vertical', spacing=30, padding=(100,30,100,0), size_hint=(1, None), pos_hint={'center_x':.5, 'top':1})
        main.cardList.bind(minimum_height=self.updateCardListSize)
        main.cardList.arr = []
        main.add_widget(main.cardList)
        self.add_widget(main)
        self.main = main

        tab = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        with tab.canvas:
            Color(.07,.07,.07,.95)
            tab.bg=RoundedRectangle(size=tab.size, radius=(30,30,0,0))
            tab.bind(size=self.updateTabSizePos)
            tab.bind(pos=self.updateTabSizePos)
        tab.add_widget(Button(text='Play', font_name='Jersey10', font_size=25, halign='center', valign='center', background_color=(0,0,0,0)))
        tab.add_widget(Button(text='AddCard', font_name='Jersey10', on_press=self.addCard, font_size=25, halign='center', valign='center', background_color=(0,0,0,0)))
        tab.add_widget(Button(text='Save', font_name='Jersey10', font_size=25, halign='center', valign='center', background_color=(0,0,0,0)))
        self.add_widget(tab)
        self.tab = tab

    def updateTitleSizePos(self, instance, value):
        instance.text_size = (.8*instance.size[0],instance.size[1])

    def updateTabSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def updateCardListSize(self, instance, value):
        instance.size[1] = instance.minimum_height

    def addCard(self, value):
        container = RelativeLayout(size_hint=(1,None), size=(0,200))

        button = Deck(disabled=False, opacity=1)
        container.add_widget(button)
        container.button = button

        card = RelativeLayout(size_hint=(0,None), size=(0, 0), disabled=True, opacity=0)

        front = BoxLayout(orientation='vertical', padding=(30), spacing=20, size_hint=(1,1))
        with front.canvas:
            Color(0,0,0,.15)
            front.shadow = BoxShadow(front.size, front.pos, offset=(0,-4), blur_radius=4.0)
            front.shadow.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            front.border = Line(rounded_rectangle=(front.pos[0],front.pos[1],front.size[0],front.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            front.bg = RoundedRectangle(size=front.size, radius=(30,30,30,30))
        front.bind(size=self.updateCardSizePos)
        front.bind(pos=self.updateCardSizePos)

        front.header = RelativeLayout(size_hint=(1, .1))
        front.header.button = Button(text='×', color=(0,0,0,1), font_size=45, size_hint=(.2, 1), pos_hint={'right':1}, on_press=(self.closeCardEdit), background_color=(0,0,0,0))
        front.header.add_widget(front.header.button)
        front.add_widget(front.header)
        
        imageLayout = RelativeLayout()
        imageLayout.input = FileChooser()
        imageLayout.image = Image(source='res/textures/img1.png', fit_mode='contain')
        imageLayout.button = Button(text='Remove', size_hint=(1,.1), size=(30,30), pos_hint={'right':1})
        # imageLayout.add_widget(imageLayout.input)
        imageLayout.add_widget(imageLayout.image)
        imageLayout.add_widget(imageLayout.button)
        front.add_widget(imageLayout)
        front.imageLayout = imageLayout

        front.input = TextInput(text='Blablabla1111', font_name='Inconsolata', font_size=25, halign='center', size_hint=(1, .2), background_color=(0,0,0,0), padding=(10,15))
        with front.canvas:
            Color(.8,.8,.8,1)
            front.input.bg = RoundedRectangle(background_color=(0,0,1,1), size=front.input.size, pos=front.input.pos, radius=(30,30,30,30))
            front.input.bind(size=self.updateCardInputSizePos)
            front.input.bind(pos=self.updateCardInputSizePos)
        front.add_widget(front.input)

        card.add_widget(front)
        card.front = front

        back = BoxLayout(orientation='vertical', padding=30, size_hint=(0,0), disabled=True, opacity=0)
        with back.canvas:
            Color(0,0,0,.15)
            back.shadow = BoxShadow(back.size, back.pos, offset=(0,-4), blur_radius=4.0)
            back.shadow.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            back.border = Line(rounded_rectangle=(back.pos[0],back.pos[1],back.size[0],back.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            back.bg = RoundedRectangle(size=back.size, radius=(30,30,30,30))
        back.bind(size=self.updateCardSizePos)
        back.bind(pos=self.updateCardSizePos)

        back.header = RelativeLayout(size_hint=(1, .1))
        back.header.button = Button(size_hint=(.2, 1), pos_hint={'right':1}, on_press=(self.closeCardEdit))
        back.header.add_widget(back.header.button)
        back.add_widget(back.header)

        back.image = Image(source='res/textures/img1.png', fit_mode='contain')
        back.add_widget(back.image)
        back.label = Label(text='Blablabla1111', font_size=25, halign='center', valign='center', size_hint=(1, .2))
        back.add_widget(back.label)
        
        card.add_widget(back)
        card.back = back

        container.add_widget(card)
        container.card = card
        
        container.button.id = len(self.main.cardList.arr)
        container.button.bind(on_press=self.openCardEdit)

        self.main.cardList.arr.append(container)
        self.main.cardList.add_widget(container)

    def openCardEdit(self, instance):
        if self.selectedCard:
            self.closeCardEdit(self)
        self.selectedCard = self.main.cardList.arr[instance.id]
        self.selectedCard.button.disabled = True
        self.selectedCard.button.opacity = 0
        self.selectedCard.button.size_hint=(0,0)
        self.selectedCard.button.size=(0, 0)

        self.selectedCard.card.disabled = False
        self.selectedCard.card.opacity = 1
        self.selectedCard.card.size_hint=(1,None)
        self.selectedCard.card.size=(0,600)

        self.selectedCard.size=(0, 600)

    def closeCardEdit(self, instance):
        self.selectedCard.button.disabled = False
        self.selectedCard.button.opacity = 1
        self.selectedCard.button.size_hint=(1,None)
        self.selectedCard.button.size=(0, 200)

        self.selectedCard.card.disabled = True
        self.selectedCard.card.opacity = 0
        self.selectedCard.card.size_hint=(0,0)
        self.selectedCard.card.size=(0,0)

        self.selectedCard.size=(0, 200)
        self.selectedCard = None

    def updatebuttonBackground(self, instance, value):
        pass

    def updateCardSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
        instance.border.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 30)
        instance.shadow.size = instance.size
        instance.shadow.pos = instance.pos

    def updateCardInputSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def toDeckList(instance, value):
        App.get_running_app().sm.current = 'DeckList'
