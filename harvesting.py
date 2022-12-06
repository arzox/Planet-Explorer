import pygame

from inventory import Inventory
from maplayers import MapLayers
from player import Player
from items import Items


class Harvesting:
    def __init__(self, map_layers: MapLayers, inventory: Inventory, player: Player):
        self.map_layers = map_layers
        self.inventory = inventory
        self.player_pos = player.position

        self.inventory.try_to_add_item_in_slot(Items.PICKAXE)
