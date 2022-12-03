import pygame
import pytmx


class IronOre(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/image/ore/iron.png').convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=pos)


class MapOres:
    def __init__(self, tmx_data: pytmx.TiledMap, all_sprite):
        self.tmx_data = tmx_data
        self.all_sprite = all_sprite
        self.tile_size = self.tmx_data.tileheight

        self.ore_grid = []
        self.ores_rect = []

        self.create_ores_grid()
        self.spawn_ore()

    def create_ores_grid(self):
        map_height, map_width = self.tmx_data.height, self.tmx_data.width
        self.ore_grid = [[[] for col in range(map_width)] for row in range(map_height)]
        for x, y, _ in self.tmx_data.get_layer_by_name("ores").tiles():
            self.ore_grid[y][x].append('O')

    def spawn_ore(self):
        for index_col, col in enumerate(self.ore_grid):
            for index_row, row in enumerate(self.ore_grid[index_col]):
                x = index_row
                y = index_col
                if 'O' in self.ore_grid[y][x]:
                    # fait apparaitre le minerai
                    ore = IronOre(pos=(x * self.tile_size, y * self.tile_size),)
                    self.all_sprite.add(ore, layer=4)
                    self.ores_rect.append(ore.rect)