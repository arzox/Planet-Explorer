import pygame
import pyscroll
from pytmx import load_pygame

import inventory
from buildLayer import BuildLayer
from inventory import Inventory
from player import Player


class Game:
    def __init__(self):
        self.group = None
        self.inventory = Inventory()
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1080, 720

        self.build_layer = None
        self.key_pressed = False

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Planet Explorer")
        self.screen = pygame.display.set_mode(self.size)
        self._running = True

        # charger la carte
        tmx_data = load_pygame('assets/map/tilemap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.size)
        map_layer.zoom = 4

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.build_layer = BuildLayer(tmx_data, self.group)

        # generer un joueur
        player_spawn = tmx_data.get_object_by_name("PlayerSpawn")
        self.player = Player([player_spawn.x, player_spawn.y], build_layer=self.build_layer)

        # definir liste de rectangle de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner groupe de calque
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        clicked = pygame.mouse.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.player.move_up()
            self.player.change_animation('up')
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.player.move_down()
            self.player.change_animation('down')
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.player.move_left()
            self.player.change_animation('left')
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.player.move_right()
            self.player.change_animation('right')

        # Pas opti
        if pressed[pygame.K_1]:
            self.inventory.select_slot(1)
        if pressed[pygame.K_2]:
            self.inventory.select_slot(2)
        if pressed[pygame.K_3]:
            self.inventory.select_slot(3)
        if pressed[pygame.K_4]:
            self.inventory.select_slot(4)
        if pressed[pygame.K_5]:
            self.inventory.select_slot(5)
        if pressed[pygame.K_6]:
            self.inventory.select_slot(6)
        if pressed[pygame.K_7]:
            self.inventory.select_slot(7)
        if pressed[pygame.K_8]:
            self.inventory.select_slot(8)
        if pressed[pygame.K_9]:
            self.inventory.select_slot(9)

        if clicked == (1, 0, 0):
            self.key_pressed = True
        elif self.key_pressed:
            self.key_pressed = False
            self.player.build()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.player.save_location()
        self.handle_input()
        self.group.update()
        if self.player.feet.collidelist(self.walls) > -1: self.player.move_back()
        self.group.center(self.player.rect)
        self.group.draw(self.screen)
        self.inventory.display(self.screen)

    def on_render(self):
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

            pygame.time.Clock().tick(60)
        self.on_cleanup()
