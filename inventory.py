from common import *
from items import Items


class Slot(pygame.sprite.Sprite):

    def __init__(self, id_slot):
        super().__init__()

        self.id_slot = id_slot
        self.counter = None
        self.item = None
        self.is_empty = True
        self.is_selected = False
        self.image = pygame.image.load('assets/inventory/default.jpg').convert()
        self.rect = self.image.get_rect()

    def set_position(self, position: (int, int)):
        self.rect.x, self.rect.y = position

    def add_item(self, item: Items):
        if self.is_empty:
            print(item.value["image"])
            self.image = pygame.image.load('assets/image/items/Pickaxe.png').convert()

            self.item = item
            self.is_empty = False
            self.counter = 1
        elif not self.is_empty and item.value["name"] == self.item:
            self.counter += 1

    def remove_item(self):
        item_removed = self.item
        self.item = None
        self.is_empty = True
        self.image = pygame.image.load('assets/inventory/default.jpg').convert()
        self.counter = 0
        return item_removed

    def select_slot(self):
        print(self.id_slot)
        if self.is_selected:
            self.is_selected = False
            self.image = pygame.image.load('assets/inventory/default.jpg').convert()
        else:
            self.is_selected = True
            self.image = pygame.image.load('assets/inventory/tile_selected.jpg').convert()

    def deselect_slot(self):
        self.is_selected = False
        self.image = pygame.image.load('assets/inventory/default.jpg').convert()


class Inventory:

    def __init__(self):
        self.selected_slot = 0
        self.slots = []

        self.create_slots()

        # Sélectionne le premier slot de l'inventaire au début du jeu
        #self.slots[0].select_slot()

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

    def try_to_add_item_in_slot(self, item):
        for slot in self.slots:
            if slot.is_empty:
                slot.add_item(item)
                break

    def get_item(self) -> Items:
        return self.slots[self.selected_slot].item

    def select_slot(self, id_slot):
        for slot in self.slots:
            if slot.id_slot == id_slot:
                slot.select_slot()
                self.selected_slot = id_slot
            else:
                slot.deselect_slot()
