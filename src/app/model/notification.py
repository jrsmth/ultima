from src.app.model.base import Base
from src.app.model.mood import Mood


# Model object that represents a notification
class Notification(Base):
    active = False
    title = ''
    content = ''
    icon = ''
    mood = Mood.NEUTRAL.value
