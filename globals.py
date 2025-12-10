from enum import Enum

class AppState(Enum):
    DECK_LIST = 0
    DECK_CREATE = 1
    CARD_LIST = 2
    CARD_EDIT = 3
    CARD_PLAY = 4
    STATISTICS = 5

class Globals:
    windowSize = (540, 960)
    currentState = AppState.DECK_LIST