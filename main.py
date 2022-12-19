from common import *

#Nom du jeu
__title__ = "The MoonGooser"
# Auteurs du jeu
__authors__ = ["Aimery", "Morgan", "Célian"]
# License du jeu
__license__ = "MIT License"
# Version du jeu
__version__ = "0.0.1"

from titlescreen import TitleScreen

class Main:

    def start(self):
        titlescreen = TitleScreen()
        titlescreen.on_execute()


if __name__ == '__main__':
    main = Main()
    main.start()


