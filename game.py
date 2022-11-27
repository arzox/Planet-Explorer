import pygame
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        self._running = True
        self._display = None
        self.size = self.weight, self.height = 1080, 720

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Planet Explorer")
        self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

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