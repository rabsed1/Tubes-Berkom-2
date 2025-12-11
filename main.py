from kivy.config import Config
from globals import Globals
Config.set('graphics', 'width', Globals.windowSize[0]*2//3)
Config.set('graphics', 'height', Globals.windowSize[1]*2//3)

Config.set('graphics', 'fullscreen', '0')
Config.set('modules', 'showborder', '')

from kivy.app import App
from kivy.core.text import LabelBase

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition

from globals import AppState
from deckList import DeckList
from cardList import CardList
from cardPlay import CardPlay
from statistics import Statistics

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Globals.currentState = AppState.STATISTICS
        LabelBase.register(name='Jersey10', fn_regular='res/fonts/Jersey10-Regular.ttf')
        LabelBase.register(name='Inconsolata', fn_regular='res/fonts/Inconsolata-VariableFont_wdth,wght.ttf')
        self.sm = ScreenManager()
        screens = [Screen() for i in range(4)]
        screens[0].name = 'DeckList'
        screens[0].add_widget(DeckList())
        screens[1].name = 'CardList'
        screens[1].add_widget(CardList())
        screens[2].name = 'CardPlay'
        screens[2].add_widget(CardPlay())
        screens[3].name = 'Statistics'
        screens[3].add_widget(Statistics())
        for i in range(4):
            self.sm.add_widget(screens[i])
        self.sm.transition = NoTransition()

        self.sm.current = 'CardList'

    def build(self):
        return self.sm

if __name__ == '__main__':
    MainApp().run()