import pygame

from common import *
from items import Items


class Slot(pygame.sprite.Sprite):

    def __init__(self, id_slot):
        super().__init__()

        self.id_slot = id_slot
        self.counter = 0
        self.item = None
        self.is_selected = False
        self.image = pygame.image.load('assets/inventory/tile.png').convert()
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont('arial', 20)

        tile_deselected = pygame.image.load('assets/inventory/tile_deselected.png').convert_alpha()
        self.image.blit(tile_deselected, tile_deselected.get_rect())

    def set_position(self, position: (int, int)):
        self.rect.x, self.rect.y = position

    def add_item(self, item: Items):
        image = pygame.image.load(item.value["inventory_icon"]).convert_alpha()
        placement = (5, 5)
        if item.value["name"] == "iron ore":
            image = pygame.transform.scale(image, (38, 38))
            placement = (12, 0)
        self.image.blit(image, placement)

        self.item = item
        self.counter = 1

    def remove_item(self):
        item_removed = self.item
        if self.counter == 0:
            self.item = None
            self.image = pygame.image.load('assets/inventory/tile.png').convert()
        else:
            self.counter -= 1
        return item_removed

    def select_slot(self):
        self.is_selected = True
        tile_selected = pygame.image.load('assets/inventory/tile_selected.png').convert_alpha()
        self.image.blit(tile_selected, self.image.get_rect())

    def deselect_slot(self):
        self.is_selected = False
        tile_deselected = pygame.image.load('assets/inventory/tile_deselected.png').convert_alpha()
        self.image.blit(tile_deselected, self.image.get_rect())

    def draw_counter(self):
        pygame.draw.rect(self.image, (255, 255, 255), (45, 45, 15, 15))
        text = self.font.render(str(self.counter), True, (0, 0, 0))
        self.image.blit(text, (50, 40))


class Inventory:

    def __init__(self):
        self.selected_slot = 0
        self.slots = []

        self.create_slots()

        # Sélectionne le premier slot de l'inventaire au début du jeu
        self.slots[0].select_slot()

    def create_slots(self):
        number = 9

        id_slot = 1
        slots_x = 100
        slots_y = 630
        for i in range(number):
            slot = Slot(id_slot)
            self.slots.append(slot)
            slot.set_position((slots_x, slots_y))
            id_slot += 1
            slots_x += 100

    def display(self, screen):
        for slot in self.slots:
            screen.blit(slot.image, slot.rect)
            slot.draw_counter()
            #pass

    def try_to_add_item_in_slot(self, item: Items):
        for slot in self.slots:
            if slot.item is None:
                slot.add_item(item)
                break
            elif slot.item == item:
                slot.counter += 1
                break

    def get_item(self) -> Items:
        return self.slots[self.selected_slot].item

    def select_slot(self, id_slot):
        for slot in self.slots:
            if slot.id_slot == id_slot:
                slot.select_slot()
            else:
                slot.deselect_slot()
