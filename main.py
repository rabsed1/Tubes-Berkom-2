from kivy.config import Config
from globals import Globals
Config.set('graphics', 'width', Globals.windowSize[0]*2//3)
Config.set('graphics', 'height', Globals.windowSize[1]*2//3)

Config.set('graphics', 'fullscreen', '0')
Config.set('modules', 'showborder', '')

from kivy.app import App

from globals import AppState
from deckList import DeckList
from cardList import CardList
from cardPlay import CardPlay

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Globals.currentState = AppState.CARD_LIST

    def build(self):
        match (Globals.currentState):
            case AppState.DECK_LIST:
                return DeckList()
            case AppState.CARD_LIST:
                return CardList()
            case AppState.CARD_PLAY:
                return CardPlay()


if __name__ == '__main__':
    MainApp().run()