import pygame

class Playerstat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.max_health = 14
        self.taux_oxygene = 7
        self.max_taux_oxygene = 7
        self.nouriture = 100
        self.max_nouriture = 100
        self.full_heart = pygame.image.load('assets/hearth/full_heart.png').convert_alpha()
        self.half_heart = pygame.image.load('assets/hearth/half_heart.png').convert_alpha()
        self.empty_heart = pygame.image.load('assets/hearth/empty_heart.png').convert_alpha()
        self.full_oxygene = pygame.image.load('assets/hearth/oxygen.png').convert_alpha()

    def get_damage(self):
        if self.health > 0:
            self.health -= 1

    def get_health(self):
        if self.health < self.max_health:
            self.health += 1

    def loose_oxy(self):
        if self.taux_oxygene > 0:
            self.taux_oxygene -= 1

    def regen_oxy(self):
        if self.taux_oxygene < self.max_taux_oxygene:
            self.taux_oxygene += 1

    def empty_hearts(self, screen):
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(self.full_heart, (heart * 50 + 10, 5))
            else:
                screen.blit(self.empty_heart, (heart * 50 + 10, 5))

    def half_hearts(self, screen):
        half_hearts_total = self.health / 2
        half_heart_exists = half_hearts_total - int(half_hearts_total) != 0

        for heart in range(int(self.max_health / 2)):
            if int(half_hearts_total) > heart:
                screen.blit(self.full_heart, (heart * 50 + 100, 570))
            elif half_heart_exists and int(half_hearts_total) == heart:
                screen.blit(self.half_heart, (heart * 50 + 100, 570))
            else:
                screen.blit(self.empty_heart, (heart * 50 + 100, 570))

    def full_hearts(self, screen):
        for heart in range(self.health):
            screen.blit(self.full_heart, (heart * 50 + 10, 45))

    def oxygene(self, screen):
        self.full_oxygene = pygame.transform.scale(self.full_oxygene, (35, 35))
        for oxy in range(self.taux_oxygene):
            screen.blit(self.full_oxygene, (oxy * 40 + 600, 570))

    def update(self, screen):
        self.half_hearts(screen)
        self.oxygene(screen)

