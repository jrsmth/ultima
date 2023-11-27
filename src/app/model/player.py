from src.app.model.base import Base


# Model object that holds the player information
class Player(Base):

    def __init__(self, name, symbol, notification):
        self.name = name
        self.symbol = symbol
        self.notification = notification
