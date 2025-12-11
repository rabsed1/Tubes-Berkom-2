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

from frontend.globals import Globals
from frontend.deck import Deck

from backend.date import tanggal_format
from backend.boxes import box_ambil
from backend.boxes import box_simpan
from backend.cards import kartu_buat

from datetime import date

class CardList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Ambil data kartu
        self.name = App.get_running_app().data['deckName']
        self.data = box_ambil(self.name)

        self.selectedCard = None
        self.flipped = False

        self.orientation='vertical'
        self.size = Globals.windowSize

        with self.canvas:
            Rectangle(source='res/textures/bg1.png', size=self.size, pos=self.pos)

        header = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        header.add_widget(Button(text='<-', color=(0,0,0,1), font_name='Jersey10', font_size=34, halign='center', valign='center', size_hint=(.2, 1), background_color=(0,0,0,0), on_press=self.toDeckList))
        title = Button(text=self.name, color=(0,0,0,1), font_name='Jersey10', font_size=34, halign='left', valign='center', background_color=(0,0,0,0))
        title.bind(size=self.updateTitleSizePos)
        header.add_widget(title)
        header.title = title
        self.add_widget(header)
        
        main = ScrollView(pos_hint={'center_x':.5}) 
        main.label = Label(text='This deck is empty...', color=(0,0,0,1), pos_hint={'center_x':.5,'center_y':.5})
        main.cardList = BoxLayout(orientation='vertical', spacing=30, padding=(100,30,100,0), size_hint=(1, None), pos_hint={'center_x':.5, 'top':1})
        main.cardList.bind(minimum_height=self.updateCardListSize)
        main.cardList.arr = []
        self.add_widget(main)
        self.main = main

        tab = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        with tab.canvas:
            Color(.07,.07,.07,.95)
            tab.bg=RoundedRectangle(size=tab.size, radius=(30,30,0,0))
            tab.bind(size=self.updateTabSizePos)
            tab.bind(pos=self.updateTabSizePos)
        tab.add_widget(Button(text='Play', font_name='Jersey10', font_size=25, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.playCard))
        tab.add_widget(Button(text='AddCard', font_name='Jersey10', font_size=25, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.addCard))
        tab.add_widget(Button(text='Save', font_name='Jersey10', font_size=25, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.saveCard))
        self.add_widget(tab)
        self.tab = tab

        # Tampilkan kartu dalam bentuk widget
        for card in self.data['kartu']:
            self.addCard(self, card)
        self.main.add_widget(main.cardList)

    def updateTitleSizePos(self, instance, value):
        instance.text_size = (.8*instance.size[0],instance.size[1])

    def updateTabSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def updateCardListSize(self, instance, value):
        instance.size[1] = instance.minimum_height

    def addCard(self, instance, data=[]):
        container = RelativeLayout(size_hint=(1,None), size=(0,200))

        button = Deck(data[0][0] if data!=[] else f'card {len(self.main.cardList.arr)}',disabled=False, opacity=1)
        container.add_widget(button)
        container.button = button

        card = RelativeLayout(size_hint=(0,None), size=(0, 0), disabled=True, opacity=0)
        card.arr = []

        for i in range(2):
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
            front.header.label = Label(text='Front' if i == 0 else 'Back', color=(0,0,0,1), font_name='Jersey10', font_size=30)
            front.header.add_widget(front.header.label)
            front.header.button = Button(text='×', color=(0,0,0,1), font_size=45, size_hint=(.2, 1), pos_hint={'right':1}, on_press=(self.closeCardEdit), background_color=(0,0,0,0))
            front.header.add_widget(front.header.button)
            front.add_widget(front.header)
            
            # imageLayout = RelativeLayout()
            # if data[i][0] != '':
            #     imageLayout.image = Image(source='res/textures/img1.png', fit_mode='contain')
            #     imageLayout.button = Button(text='Remove', size_hint=(1,.1), size=(30,30), pos_hint={'right':1})
            #     imageLayout.add_widget(imageLayout.image)
            #     imageLayout.add_widget(imageLayout.button)
            # else:
            #     imageLayout.input = FileChooser()
            #     imageLayout.add_widget(imageLayout.input)
            # front.add_widget(imageLayout)
            # front.imageLayout = imageLayout

            front.input = TextInput(text=data[i][0] if data!=[] else f'card {len(self.main.cardList.arr)}', font_name='Inconsolata', font_size=25, halign='center', size_hint=(1, 1), background_color=(0,0,0,0), padding=(10,15))
            with front.canvas:
                Color(.8,.8,.8,1)
                front.input.bg = RoundedRectangle(background_color=(0,0,1,1), size=front.input.size, pos=front.input.pos, radius=(30,30,30,30))
                front.input.bind(size=self.updateCardInputSizePos)
                front.input.bind(pos=self.updateCardInputSizePos)
            front.add_widget(front.input)
            front.add_widget(Button(text='Flip card', color=(0,0,0,1), size_hint=(1,.1), background_color=(0,0,0,0), on_press=self.flipCard))

            card.add_widget(front)
            card.arr.append(front)
        
        card.arr[1].disabled = True
        card.arr[1].opacity = 0
        card.arr[1].size_hint = (0,0)

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
        self.selectedCard.card.size=(0,400)

        self.selectedCard.size=(0, 400)

    def closeCardEdit(self, instance):
        if self.selectedCard.card.arr[0].input.text != '':
            self.selectedCard.button.updateTitle(self, self.selectedCard.card.arr[0].input.text)
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
        self.flipped = False

    def flipCard(self, instance):
        self.selectedCard.card.arr[self.flipped].disabled = True
        self.selectedCard.card.arr[self.flipped].size_hint = (0,0)
        self.selectedCard.card.arr[self.flipped].opacity = 0
        self.selectedCard.card.arr[not self.flipped].disabled = False
        self.selectedCard.card.arr[not self.flipped].size_hint = (1,1)
        self.selectedCard.card.arr[not self.flipped].opacity = 1
        self.flipped = not self.flipped


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
        App.get_running_app().SwitchScreen(0, {})

    def playCard(self, instance):
        App.get_running_app().SwitchScreen(2, {'deckName': self.name})

    def saveCard(self, instance):
        cards = []
        for card in self.main.cardList.arr:
            cards.append(kartu_buat([card.card.arr[0].input.text],[card.card.arr[1].input.text],tanggal_format(date.today())))
        box_simpan(self.name, cards)
