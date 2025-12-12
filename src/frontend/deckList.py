from kivy.app import App

from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle

from datetime import date

from frontend.globals import Globals
from frontend.globals import AppState
from frontend.deck import Deck

from backend.date import tanggal_format
from backend.boxes import box_buat
from backend.boxes import boxes_daftar_nama
from backend.boxes import box_ambil

class DeckList(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size=Globals.windowSize

        self.focusDeck = None
        
        self.addDeckMenu = None
        self.deckTab = None
        self.blurLayer = None

        container = BoxLayout(orientation='vertical', spacing=30, padding=(0,20,0,0))

        with self.canvas:
            Rectangle(source='res/textures/bg1.png', size=self.size)

        title = Label(text='Decks', font_name='Jersey10', font_size=55, color=(0,0,0,1), size_hint=(1, .2), pos_hint={'center_x':.5})
        container.add_widget(title)
        container.title = title

        button = Button(text='+   Add Deck', font_name='Jersey10', font_size=28, color=(0,0,0,1), size_hint=(.4, .1), pos_hint={'center_x':.5}, background_color=(0,0,0,0))
        button.bind(on_press=self.showAddDeckMenu)
        container.add_widget(button)
        container.button = button

        deckList = ScrollView()
        dlContainer = BoxLayout(orientation='vertical', size_hint=(1,None), padding=(100,0), spacing=40, pos_hint={'center_x':.5,'top':1})
        dlContainer.arr = []
        dlContainer.bind(minimum_height=self.updateDeckListSize)

        deckList.add_widget(dlContainer)
        deckList.container = dlContainer
        
        container.add_widget(deckList)
        container.deckList = deckList

        self.add_widget(container)
        self.container = container

        self.initDeckList()
    
    def initDeckList(self):
        self.container.deckList.container.clear_widgets()
        self.container.deckList.container.arr.clear()
        for name in boxes_daftar_nama():
            data = box_ambil(name)
            deck = Deck(name)
            deck.bind(on_press=self.showDeckTab)
            self.container.deckList.container.add_widget(deck)
            self.container.deckList.container.arr.append(deck)

    def updateDeckListSize(self, instance, value):
        self.container.deckList.container.size[1] = instance.minimum_height
    
    def showAddDeckMenu(instance, value):
        if not instance.addDeckMenu:
            addDeckMenu = RelativeLayout(size_hint=(.75,.75), pos_hint={'center_x':.5, 'center_y':.5})
            with addDeckMenu.canvas:
                Color(1,1,1,1)
                addDeckMenu.bg = RoundedRectangle(size=addDeckMenu.size, radius=(30,30,30,30))
                addDeckMenu.bgImage = RoundedRectangle(source='res/textures/bg2.png', pos=(0, addDeckMenu.size[1]), size=(addDeckMenu.size[0], 0.4*addDeckMenu.size[1]), radius=(30,30,30,30))
                addDeckMenu.bind(size=instance.updateAddDeckMenuSizePos)
                addDeckMenu.bind(pos=instance.updateAddDeckMenuSizePos)

            input = TextInput(hint_text='Add deck name...', font_name='Jersey10', font_size=25, size_hint=(.8, .2), pos_hint={'center_x':.5, 'y':.5}, multiline=False, background_color=(0,0,0,0), padding=(30,30,30,30))
            with addDeckMenu.canvas:
                Color(.8,.8,.8,1)
                input.bg = RoundedRectangle(background_color=(0,0,1,1), size=input.size, pos=input.pos, radius=(30,30,30,30))
                input.bind(size=instance.updateAddDeckMenuInputSizePos)
                input.bind(pos=instance.updateAddDeckMenuInputSizePos)
            addDeckMenu.add_widget(input)
            addDeckMenu.input = input

            btnOk = Button(text='Ok', font_name='Jersey10', font_size=32, size_hint=(.5, .1), pos_hint={'center_x':.25, 'y':0}, color=(0,0,0,1), background_color=(0,0,0,0))
            btnOk.bind(on_press=instance.addDeck)
            addDeckMenu.add_widget(btnOk)
            addDeckMenu.btnOk = btnOk

            btnCancel = Button(text='Cancel', font_name='Jersey10', font_size=32, size_hint=(.5,.1), pos_hint={'center_x':.75, 'y':0}, color=(0,0,0,1), background_color=(0,0,0,0))
            btnCancel.bind(on_press=instance.closeAddDeckMenu)
            addDeckMenu.add_widget(btnCancel)
            addDeckMenu.btnCancel = btnCancel

            instance.add_widget(addDeckMenu)
            instance.addDeckMenu = addDeckMenu
    
    def closeAddDeckMenu(instance, value):
        instance.remove_widget(instance.addDeckMenu)
        instance.addDeckMenu = None

    def showDeckTab(self, instance):
        self.focusDeck = instance
        if not self.deckTab:
            self.addBlurLayer()
            layout = BoxLayout(orientation='vertical', size_hint=(1, .22))
            with layout.canvas:
                Color(.07,.07,.07,.95)
                layout.bg=RoundedRectangle(size=layout.size, radius=(30,30,0,0))
                layout.bind(size=self.updateDeckTabSizePos)
                layout.bind(pos=self.updateDeckTabSizePos)
            layout.add_widget(Button(text='------', size_hint=(1,.5), font_size=30, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.removeBlurLayer))
            layout.add_widget(Button(text='Open Deck', font_name='Jersey10', font_size=27, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.toCardList))
            layout.add_widget(Button(text='Rename', font_name='Jersey10', font_size=27, halign='center', valign='center', background_color=(0,0,0,0)))
            layout.add_widget(Button(text='Delete', font_name='Jersey10', font_size=27, halign='center', valign='center', background_color=(0,0,0,0)))
            self.add_widget(layout)
            self.deckTab = layout

    def addBlurLayer(instance):
        if not instance.blurLayer:
            layout = Button(size_hint=(1, 1), background_color=(0,0,0,0))

            layout.bind(on_press=instance.removeBlurLayer)

            instance.add_widget(layout)
            instance.blurLayer = layout

    def removeBlurLayer(instance, value):
        if instance.blurLayer:
            instance.focusDeck = None
            instance.remove_widget(instance.blurLayer)
            instance.remove_widget(instance.deckTab)
            instance.blurLayer = None
            instance.deckTab = None

    def toCardList(self, instance):
        App.get_running_app().SwitchScreen(1, {'deckName': self.focusDeck.title})

    def addDeck(instance, value):
        deck = Deck(instance.addDeckMenu.input.text)
        deck.bind(on_press=instance.showDeckTab)
        instance.container.deckList.container.add_widget(deck)
        instance.container.deckList.container.arr.append(deck)

        box_buat(instance.addDeckMenu.input.text, tanggal_format(date.today()))
        instance.closeAddDeckMenu(0)

    def updateAddDeckMenuSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bgImage.size = (instance.size[0],.4*instance.size[1])
        instance.bgImage.pos = (0, instance.size[1]-instance.bgImage.size[1])

    def updateAddDeckMenuInputSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos

    def updateDeckTabSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos