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
        self.speed = 3

    def update(self):
        self.rect.topleft = self.position

    def move_right(self): self.position[0] += self.speed
    def move_left(self): self.position[0] -= self.speed
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed
    def getImage(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image