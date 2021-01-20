from abc import ABC, abstractmethod


class Service(ABC):
    # Dummy class, TODO change this class and its methods
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def plugin_id(self) -> int:
        pass


class LoadDataService(Service):
    # Dummy class, TODO change this class and its methods
    def __init__(self):
        super().__init__()

    @abstractmethod
    def load_data(self, path) -> str:
        #povratna vrednost Graph
        pass



class VisualizeService(Service):
    # Dummy class, TODO change this class and its methods
    def __init__(self):
        super().__init__()



