import pygame
import maplayers


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, build_layer: maplayers.MapLayers):
        super().__init__()
        self.sprite_sheet = pygame.image.load('assets/player/playerSpriteSheet.png').convert_alpha()
        self.position = pos
        self.images = {
            'down': self.getImage(0, 0),
            'left': self.getImage(0, 32),
            'right': self.getImage(0, 64),
            'up': self.getImage(0, 96)
        }
        self.image = self.images['down']
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.speed = 3
        self.feet = pygame.Rect(0, 0, self.rect.width / 3, 12)
        self.detect_rect = pygame.Rect(0, 0, self.rect.width * 1.5, self.rect.height * 1.5)
        self.old_position = self.position.copy()

        # interactions
        self.build_layer = build_layer

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.detect_rect.center = self.rect.center

        direction = list(self.images.keys())[list(self.images.values()).index(self.image)]
        self.build_layer.set_build_position(direction, self.position)

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.detect_rect.center = self.rect.center

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def getImage(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
