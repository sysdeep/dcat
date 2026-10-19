from abc import ABC, abstractmethod


class MainMenuHandler(ABC):
    @abstractmethod
    def backup_db(self):
        pass

    @abstractmethod
    def show_find_modal(self):
        pass

    @abstractmethod
    def show_open_db(self):
        pass

    @abstractmethod
    def show_create_db(self):
        pass

    @abstractmethod
    def show_add_volume(self):
        pass
