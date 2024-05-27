from abc import ABCMeta, abstractmethod

class GameState(metaclass=ABCMeta):
    @abstractmethod
    def enterState(self):
        pass

    @abstractmethod
    def exitState(self):
        pass

    @abstractmethod
    def event(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
