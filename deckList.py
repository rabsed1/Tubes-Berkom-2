from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle

from globals import Globals
from globals import AppState

from deck import Deck

class DeckList(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size=Globals.windowSize
        layout = GridLayout(cols=1, spacing=(0, 50), size_hint=(1, None), size=(0, self.size[1]))
        with layout.canvas:
            layout.rect = Rectangle(source='res/texture/bg1.png', size=layout.size)
            layout.bind(size=self.updateDeckBackground)

        self.decks = RelativeLayout(size_hint=(1,None))
        self.decks.layout = GridLayout(cols=1, size_hint=(.7, None), spacing=(0,40), pos_hint={'center_x':.5,'top':1})
        for i in range(1):
            deck = Deck()
            deck.bind(on_press=self.showDeckTab)
            self.decks.layout.add_widget(deck)
        self.decks.add_widget(self.decks.layout)
        self.decks.layout.bind(size=self.updateDeckSize)
        
        lblDeck = Label(text='Decks', font_size=48, color=(0,0,0,1), size_hint=(1, None), size=(0,75), pos_hint={'center_x':.5})
        btnAddDeck = Button(text='+   Add Deck', font_size=22, color=(0,0,0,1), size_hint=(.4, None), size=(0,50), pos_hint={'center_x':.5}, background_color=(0,0,0,0))
        btnAddDeck.bind(on_press=self.showAddDeckMenu)
        layout.add_widget(lblDeck)
        layout.add_widget(btnAddDeck)
        layout.add_widget(self.decks)
        self.layout = layout
        self.add_widget(self.layout)

        self.addDeckMenu = None
        self.deckTab = None
        self.blurLayer = None

    def transitionToCardList(instance, value):
        Globals.currentState = AppState.CARD_LIST
    
    def updateDeckSize(self, instance, value):
        self.decks.size[1] = instance.minimum_height
        print(self.decks.size)

    def updateDeckBackground(self, instance, value):
        self.layout.rect.size = instance.size
    
    def showAddDeckMenu(instance, value):
        if not instance.addDeckMenu:
            layout = RelativeLayout(size_hint=(.75,.75), pos_hint={'center_x':.5, 'center_y':.5})
            with layout.canvas:
                Color(1,1,1,1)
                layout.rect1 = RoundedRectangle(size=layout.size, radius=(30,30,30,30))
                layout.rect2 = RoundedRectangle(source='res/texture/bg2.png', pos=(0, layout.size[1]), size=(layout.size[0], 0.4*layout.size[1]), radius=(30,30,30,30))
                layout.bind(size=instance.updateAddDeckMenuBackground)
                layout.bind(pos=instance.updateAddDeckMenuBackground)

            layout.tiTitle = TextInput(hint_text='Add deck name...', font_size=20, size_hint=(.8, .2), pos_hint={'center_x':.5, 'y':.5}, multiline=False, background_color=(0,0,0,0), padding=(30,30,30,30))
            with layout.canvas:
                Color(.8,.8,.8,1)
                layout.rect3 = RoundedRectangle(background_color=(0,0,1,1), size=layout.tiTitle.size, pos=layout.tiTitle.pos, radius=(30,30,30,30))
                layout.tiTitle.bind(size=instance.updateTiTitleBackground)
                layout.tiTitle.bind(pos=instance.updateTiTitleBackground)

            instance.btnOk = Button(text='Ok', font_size=30, size_hint=(.5, .1), pos_hint={'center_x':.25, 'y':0}, color=(0,0,0,1), background_color=(0,0,0,0))
            instance.btnCancel = Button(text='Cancel', font_size=30, size_hint=(.5,.1), pos_hint={'center_x':.75, 'y':0}, color=(0,0,0,1), background_color=(0,0,0,0))
            instance.btnCancel.bind(on_press=instance.closeAddDeckMenu)
            instance.btnOk.bind(on_press=instance.addDeck)

            layout.add_widget(layout.tiTitle)
            layout.add_widget(instance.btnCancel)
            layout.add_widget(instance.btnOk)

            instance.addDeckMenu = layout
            instance.add_widget(instance.addDeckMenu)
    
    def closeAddDeckMenu(instance, value):
        instance.remove_widget(instance.addDeckMenu)
        instance.addDeckMenu = None

    def showDeckTab(instance, value):
        if not instance.deckTab:
            instance.addBlurLayer()
            layout = GridLayout(size_hint=(1, .22), cols=1, rows=4)
            with layout.canvas:
                Color(.07,.07,.07,.95)
                layout.rect1=RoundedRectangle(size=layout.size, radius=(30,30,0,0))
                layout.bind(size=instance.updateDeckTabBackground)
                layout.bind(pos=instance.updateDeckTabBackground)
            layout.add_widget(Button(text='------', size_hint=(1,.5), font_size=30, halign='center', valign='center', background_color=(0,0,0,0), on_press=instance.removeBlurLayer))
            layout.add_widget(Button(text='Open Deck', font_size=30, halign='center', valign='center', background_color=(0,0,0,0), on_press=instance.transitionToCardList))
            layout.add_widget(Button(text='Rename', font_size=30, halign='center', valign='center', background_color=(0,0,0,0)))
            layout.add_widget(Button(text='Delete', font_size=30, halign='center', valign='center', background_color=(0,0,0,0)))
            instance.add_widget(layout)
            instance.deckTab = layout

    def addBlurLayer(instance):
        if not instance.blurLayer:
            layout = Button(size_hint=(1, 1), background_color=(0,0,0,0))

            layout.bind(on_press=instance.removeBlurLayer)

            instance.add_widget(layout)
            instance.blurLayer = layout

    def removeBlurLayer(instance, value):
        if instance.blurLayer:
            instance.remove_widget(instance.blurLayer)
            instance.remove_widget(instance.deckTab)
            instance.blurLayer = None
            instance.deckTab = None

    def addDeck(instance, value):
        deck = Deck()
        deck.bind(on_press=instance.showDeckTab)
        instance.decks.layout.add_widget(deck)
        instance.closeAddDeckMenu(0)
    
    def updateAddDeckMenuBackground(self, instance, value):
        self.addDeckMenu.rect1.size = instance.size
        self.addDeckMenu.rect2.size = (instance.size[0], 0.4*instance.size[1])
        self.addDeckMenu.rect2.pos = (0, 0.6*instance.size[1])

    def updateTiTitleBackground(self, instance, value):
        self.addDeckMenu.rect3.size = instance.size
        self.addDeckMenu.rect3.pos = instance.pos

    def updateDeckTabBackground(self, instance, value):
        self.deckTab.rect1.size = instance.size
        self.deckTab.rect1.pos = instance.pos