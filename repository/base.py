from abc import ABC, abstractmethod
from database.session import Session


class BaseRepository(ABC):
    def __init__(self, session: Session):
        self.session: Session = session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
