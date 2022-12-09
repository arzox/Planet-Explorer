import pygame
from pyscroll import PyscrollGroup

from inventory import Inventory
from maplayers import MapLayers, IronOre
from player import Player


class Harvesting:
    def __init__(self, map_layers: MapLayers, inventory: Inventory, player: Player, all_sprites: PyscrollGroup):
        self.map_layers = map_layers
        self.inventory = inventory
        self.player = player
        self.all_sprites = all_sprites

        self.digging_time = 0
        self.collide_ore = -1

    def digging(self):
        collide_ore = self.player.detect_rect.collidelist(self.map_layers.ores_rect)
        if - 1 < collide_ore:
            if self.digging_time == 0:
                self.digging_time += 0.1
                self.collide_ore = collide_ore

                # lancement de la couroutine
                self.digging = self.print_name()

            elif collide_ore == self.collide_ore:
                self.digging_time += 0.1
                #next(self.digging)
                if self.digging_time >= 10:
                    self.all_sprites.get_sprites_from_layer(4)[collide_ore].kill()
                    self.map_layers.ores_rect.pop(collide_ore)
                    self.digging_time = 0
                    self.digging.close()
        else:
            self.stop_digging()

    def print_name(self):
        while True:
            yield
            print("5")

    def stop_digging(self):
        self.digging_time = 0
