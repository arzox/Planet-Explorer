import pygame.event

from common import *
from game import Game


class TitleScreen:
    def __init__(self):
        self.is_running = None
        self.screen = None
        self.size = self.weight, self.height = 1080, 720
        text = sans_font.render("The GoosMooner", True, (255, 255, 255))
        goose = pygame.image.load("assets/player/goose.png").convert_alpha()

        # Crée l'image du titre et le centre sur l'écran
        title_size = (576, 64)
        self.title = pygame.Surface(title_size)
        self.title.blit(goose, (0, 0))
        self.title.blit(text, (64, -16))
        self.title.blit(goose, (title_size[0] - 55, 0))
        self.title_position = (250, 100)

        # Menu principal et boutons
        button_size = (256, 64)
        self.menu = pygame.sprite.Group()
        self.menu.add(
            PushButton("Nouvelle Partie", button_size, (300, 288), self.play),
            PushButton("Quitter Jeu", button_size, (600, 288), self.stop)
        )

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Planet Explorer")
        self.screen = pygame.display.set_mode(self.size)
        self.is_running = True

    def play(self):
        game = Game()
        game.on_execute()
        self.is_running = False


    def on_event(self, event):
        self.menu.update(event)

    def render(self):
        pygame.display.flip()
        screen.blit(self.title, self.title_position)
        self.menu.draw(self.screen)

    def stop(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        self.on_init()
        while self.is_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.render()
            pygame.time.Clock().tick(60)
        self.stop()
