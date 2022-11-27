import pygame
from pytmx.util_pygame import load_pygame
import pyscroll
from player import Player
import scipy


class Game:
    def __init__(self):
        self._running = True
        self.screen = None
        self.size = self.weight, self.height = 1080, 720

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Planet Explorer")
        self.screen = pygame.display.set_mode(self.size)
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
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.handle_input()
        self.group.update()
        self.group.center(self.player.rect)
        self.group.draw(self.screen)

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