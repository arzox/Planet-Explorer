import pygame
from pyscroll import PyscrollGroup

from items import Items


class DropItem(pygame.sprite.Sprite):
    def __init__(self, pos, image_adress, item: Items):
        super().__init__()
        self.image = pygame.image.load(image_adress).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.item = item


class Drops:
    def __init__(self, all_sprites: PyscrollGroup):
        self.all_sprites = all_sprites
        self.items_rect = []

    def drop_item(self, image_adress, pos, item: Items):
        sprite = DropItem(image_adress, pos, item)
        self.items_rect.append(sprite.rect)
        self.all_sprites.add(sprite, layer=7)

    def get_item(self, sprite_number):
        sprite = self.all_sprites.get_sprites_from_layer(7)[sprite_number]
        item = sprite.item
        sprite.kill()

