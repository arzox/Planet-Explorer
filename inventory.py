import pygame


class Slot(pygame.sprite.Sprite):

    def __init__(self, id_slot):
        super().__init__()

        self.id_slot = id_slot
        self.counter = None
        self.item_in_slot = None
        self.is_empty = True
        self.is_selected = False
        self.image = pygame.image.load('assets/inventory/default.jpg')
        self.rect = self.image.get_rect()

    def set_position(self, position: (int, int)):
        self.rect.x, self.rect.y = position

    def add_item(self, item):
        if self.is_empty is True:
            self.item_in_slot = item
            self.is_empty = False
            self.counter = 1
        elif self.is_empty is False and item.type == self.item_in_slot:
            self.counter += 1

    def remove_item(self):
        item_removed = self.item_in_slot
        if self.counter > 1:
            self.counter -= 1
        else:
            self.item_in_slot = None
            self.is_empty = True
            self.counter = None
        return item_removed

    def select_slot(self):
        self.image = pygame.image.load('assets/inventory/tile_selected.jpg')

    def deselect_slot(self):
        self.image = pygame.image.load('assets/inventory/default.jpg')


class Inventory:

    def __init__(self):

        self.number = 9
        self.slots = []

        id_slot = 1
        slots_x = 100
        slots_y = 630
        for i in range(self.number):
            slot = Slot(id_slot)
            self.slots.append(slot)
            slot.set_position((slots_x, slots_y))
            id_slot += 1
            slots_x += 100

        # Sélectionne le premier slot de l'inventaire au début du jeu
        self.slots[0].select_slot()
        self.slots[0].is_selected = True

    def display(self, screen):
        for slot in self.slots:
            screen.blit(slot.image, slot.rect)

    def try_to_add_item_in_slot(self, item):
        id_slot = 1
        while True or id_slot <= 9:
            slot = Slot(id_slot)
            if slot.is_empty is True:
                slot.add_item(item)
                break
            else:
                id_slot += 1

    def select_slot(self, id_slot):
        for slot in self.slots:
            if slot.id_slot == id_slot:
                slot.select_slot()
                slot.is_selected = True
            else:
                slot.deselect_slot()
                slot.is_selected = False
