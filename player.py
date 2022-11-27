import pygame
import scipy

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('assets/player/playerSpriteSheet.png')
        self.image = self.getImage(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.position = [x,y]
        self.images = {
            'down': self.getImage(0,0),
            'left': self.getImage(0,32),
            'right': self.getImage(0, 64),
            'up': self.getImage(0, 96)
        }
        self.speed = 3
        self.feet = pygame.Rect(0, 0, self.rect.width/2, 12)
        self.old_position = self.position.copy()

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def save_location(self): self.old_position = self.position.copy()
    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def move_right(self): self.position[0] += self.speed
    def move_left(self): self.position[0] -= self.speed
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed
    def getImage(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image