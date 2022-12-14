from common import *

import items
from drop import Drops
from inventory import Inventory
from maplayers import MapLayers, IronOre
from player import Player


class Harvesting:
    def __init__(self, map_layers: MapLayers, inventory: Inventory, player: Player, all_sprites: PyscrollGroup, drop: Drops):
        self.map_layers = map_layers
        self.inventory = inventory
        self.player = player
        self.all_sprites = all_sprites
        self.drop = drop

        self.digging_time = 0
        self.collide_ore = -1

    def digging(self):
        collide_ore = self.player.detect_rect.collidelist(self.map_layers.ores_rects)
        if - 1 < collide_ore:
            if self.digging_time == 0:
                self.digging_time += 0.1
                self.collide_ore = collide_ore
                # lancement de la couroutine
                self.digging_couroutine = self.digging_animation(self.all_sprites.get_sprites_from_layer(4)[collide_ore])

            elif collide_ore == self.collide_ore:
                self.digging_time += 0.1
                next(self.digging_couroutine)
                if self.digging_time >= 10:
                    self.finsish_digging()
        else:
            self.stop_digging()

    def finsish_digging(self):
        self.all_sprites.get_sprites_from_layer(4)[self.collide_ore].kill()
        self.stop_digging()
        self.digging_couroutine.close()

        self.drop.drop_item(self.map_layers.ores_rects[self.collide_ore].topleft, items.Items.IRON_ORE)
        self.map_layers.ores_rects.pop(self.collide_ore)

    def stop_digging(self):
        self.digging_time = 0

    def digging_animation(self, ore: pygame.sprite):
        start_pos = ore.rect.topleft
        offset = (0, 0)
        is_moving_right = random.choice([True, False])
        while True:
            yield
            if is_moving_right:
                offset = offset[0] + 0.5, 0
                if offset[0] >= 1:
                    is_moving_right = False
            else:
                offset = offset[0] - 0.5, 0
                if offset[0] <= -1:
                    is_moving_right = True

            ore.position = start_pos[0] + offset[0], start_pos[1] + offset[1]
