from kivy.config import Config
from frontend.globals import Globals
Config.set('graphics', 'width', Globals.windowSize[0]*2//3)
Config.set('graphics', 'height', Globals.windowSize[1]*2//3)

Config.set('graphics', 'fullscreen', '0')
Config.set('modules', 'showborder', '')

from kivy.app import App
from kivy.core.text import LabelBase

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition

from frontend.globals import AppState
from frontend.deckList import DeckList
from frontend.cardList import CardList
from frontend.cardPlay import CardPlay
from frontend.statistics import Statistics

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Globals.currentState = AppState.STATISTICS
        LabelBase.register(name='Jersey10', fn_regular='res/fonts/Jersey10-Regular.ttf')
        LabelBase.register(name='Inconsolata', fn_regular='res/fonts/Inconsolata-VariableFont_wdth,wght.ttf')
        self.sm = ScreenManager()
        self.sm.transition = NoTransition()

    def build(self):
        screen = Screen(name='0')
        screen.add_widget(DeckList())
        self.sm.add_widget(screen)
        return self.sm

    def SwitchScreen(self, idx, data):
        self.sm.clear_widgets()

        self.data = data
        match idx:
            case 0:
                screen = Screen(name='0')
                screen.add_widget(DeckList())
                self.sm.add_widget(screen)
            case 1:
                screen = Screen(name='1')
                screen.add_widget(CardList())
                self.sm.add_widget(screen)
            case 2:
                screen = Screen(name='2')
                screen.add_widget(CardPlay())
                self.sm.add_widget(screen)
            case 3:
                screen = Screen(name='3')
                screen.add_widget(Statistics())
                self.sm.add_widget(screen)
        self.sm.current = screen.name

if __name__ == '__main__':
    MainApp().run()