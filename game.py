import pygame
from pytmx.util_pygame import load_pygame
import pyscroll
from player import Player


class Game:
    def __init__(self):
        self._running = True
        self._display = None
        self.size = self.weight, self.height = 1080, 720

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Planet Explorer")
        self._display = pygame.display.set_mode(self.size)
        self._running = True

        #charger la carte
        tmx_data = load_pygame('assets/map/tilemap.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.size)
        map_layer.zoom = 4

        #generer un joueur
        player_spawn = tmx_data.get_object_by_name("PlayerSpawn")
        self.player = Player(player_spawn.x,player_spawn.y)

        #dessiner groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            print("haut")
        elif pressed[pygame.K_DOWN]:
            print("bas")
        elif pressed[pygame.K_LEFT]:
            print("gauche")
        elif pressed[pygame.K_RIGHT]:
            print("droite")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.group.update()
        self.group.center(self.player.rect)
        self.group.draw(self._display)

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
        self.on_cleanup()