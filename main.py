import pygame
from pytmx.util_pygame import load_pygame
from game import Game

if __name__ == "__main__":
    game = Game()
    game.on_execute()