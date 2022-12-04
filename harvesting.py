import pygame

from inventory import Inventory
from maplayers import MapLayers
from player import Player


class Harvesting:
    def __init__(self, map_layers: MapLayers, inventory: Inventory, player: Player):
        self.map_layers = map_layers
        self.inventory = inventory
        self.player_pos = player.position
