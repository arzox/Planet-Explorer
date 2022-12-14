from game import Game
#Nom du jeu
__title__ = "The MoonGooser"
# Auteurs du jeu
__authors__ = ["Aimery", "Morgan", "Célian"]
# License du jeu
__license__ = "MIT License"
# Version du jeu
__version__ = "0.0.1"

if __name__ == '__main__':
    game = Game()
    game.on_execute()