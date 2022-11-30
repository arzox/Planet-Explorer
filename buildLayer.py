import pygame
import pytmx
from build import Build


class HoloTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.image = surf
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(topleft=pos)


class BuildLayer:
    def __init__(self, tmx_data: pytmx.TiledMap, all_sprites):
        self.tmx_data = tmx_data
        self.all_sprites = all_sprites
        self.tile_size = self.tmx_data.tileheight
        # sprite groups
        self.plan_sprites = pygame.sprite.Group()

        # graphics
        # self.plan_surf = pygame.image.load(plan.value)

        self.create_ground_grid()
        self.create_ground_rects()

    def create_ground_grid(self):
        map_height, map_width = self.tmx_data.height, self.tmx_data.width

        self.grid = [[[] for col in range(map_width)] for row in range(map_height)]
        for x, y, _ in self.tmx_data.get_layer_by_name("ground").tiles():
            self.grid[y][x].append('B')

    def create_ground_rects(self):
        self.ground_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'B' in cell:
                    x = index_col * self.tile_size
                    y = index_row * self.tile_size
                    rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    self.ground_rects.append(rect)

    def get_build(self, point):
        for rect in self.ground_rects:
            if rect.collidepoint(point):
                x = round(rect.x / self.tile_size)
                y = round(rect.y / self.tile_size)

                if 'B' in self.grid[y][x] and not 'X' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_build()

    def create_build(self):
        self.plan_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    print(self.all_sprites)
                    sprite = HoloTile(pos=(index_col * self.tile_size, index_row * self.tile_size), surf=pygame.image.load(Build.HOLO.value),)
                    self.all_sprites.add(sprite)
