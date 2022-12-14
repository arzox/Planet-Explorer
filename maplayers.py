import pygame
import pytmx
from building import Building


# Sprite qui contient les batiments
class BuildTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.image = surf
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)


class IronOre(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/image/ore/iron.png').convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.position = pos
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.rect.topleft = self.position


# Sprite de la visualisation de construction
class BuildPreviewTile(pygame.sprite.Sprite):
    def __init__(self, surf, instance):
        super().__init__()

        # creation sprite
        self.image = surf
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(topleft=[0, 0])

        # variables temporaires
        self.build_instance = instance
        self.is_buildable = False
        self.is_preview = False

    # fonction appele a chaque update du group de calque
    def update(self):
        # actualise la position
        self.rect.topleft = self.build_instance.build_position

        # change la couleur en fonction de la zone de construction
        if self.is_preview:
            self.is_buildable = self.build_instance.check_buildable()
            self.set_color()

    def set_color(self):
        if self.is_buildable:
            self.image.fill((10, 255, 235))
        else:
            self.image.fill((255, 0, 0))


# class qui gere la construction
class MapLayers:
    def __init__(self, tmx_data: pytmx.TiledMap, all_sprite):
        # recupere valeur de la carte
        self.tmx_data = tmx_data
        self.all_sprite = all_sprite
        self.tile_size = self.tmx_data.tileheight

        self.build_rects = []
        self.ores_rects = []
        self.walls_rects = []

        # creer la tile de previsualisation
        self.build_position = [0, 0]
        self.build_preview_tile = BuildPreviewTile(pygame.image.load(Building.HOLO.value).convert(), self)

        self.create_map_layer_grid()
        self.spawn_ore()
        self.create_walls_rect()

    # creer une table de la carte avec les tiles de sol
    def create_map_layer_grid(self):
        map_height, map_width = self.tmx_data.height, self.tmx_data.width
        self.grid = [[[] for col in range(map_width)] for row in range(map_height)]
        for x, y, _ in self.tmx_data.get_layer_by_name("ground").tiles():
            self.grid[y][x].append('B')
        for x, y, _ in self.tmx_data.get_layer_by_name("ores").tiles():
            self.grid[y][x].append('O')

    def create_walls_rect(self):
        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.walls_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # verifie si le build est possible
    def check_buildable(self):
        x = self.build_position[0] // self.tile_size
        y = self.build_position[1] // self.tile_size

        if 0 <= y < len(self.grid):
            if 0 <= x < len(self.grid[y]):
                if 'B' in self.grid[y][x] and not ('X' in self.grid[y][x] or 'O' in self.grid[y][x]):
                    return True
        return False

    # fait apparaitre un batiment au coordonnees
    def set_build(self):
        x = self.build_position[0] // self.tile_size
        y = self.build_position[1] // self.tile_size
        if self.check_buildable():
            # fait apparaitre le sprite et empeche la creation d'un batiment au même endroit
            self.grid[y][x].append('X')
            sprite = BuildTile(pos=(x * self.tile_size, y * self.tile_size),
                               surf=pygame.image.load(Building.HOLO.value).convert())
            self.build_rects.append(sprite.rect)
            self.all_sprite.add(sprite, layer=5)

    def spawn_ore(self):
        for index_col, col in enumerate(self.grid):
            for index_row, row in enumerate(self.grid[index_col]):
                x = index_row
                y = index_col
                if 'O' in self.grid[y][x]:
                    # fait apparaitre le minerai
                    ore = IronOre(pos=(x * self.tile_size, y * self.tile_size), )
                    self.all_sprite.add(ore, layer=4)
                    self.ores_rects.append(ore.rect)

    # fait apparaitre la previsualisation
    def set_build_preview(self):
        self.all_sprite.add(self.build_preview_tile, layer=9)
        self.build_preview_tile.is_preview = True

    # fait disparaitre la previsualisation
    def remove_build_preview(self):
        self.all_sprite.remove(self.build_preview_tile)
        self.build_preview_tile.is_preview = False

    # creer une position pour les tiles en fonction de ou regarde le joueur
    def set_build_position(self, direction: str, position: list):
        match direction:
            case "right":
                self.build_position = [round((position[0] + self.tile_size * 3) / self.tile_size) * self.tile_size,
                                       round((position[1] + self.tile_size - 8) / self.tile_size) * self.tile_size]
            case "down":
                self.build_position = [round((position[0]) / self.tile_size) * self.tile_size,
                                       round((position[1] + self.tile_size * 3) / self.tile_size) * self.tile_size]
            case "left":
                self.build_position = [round((position[0] - self.tile_size * 2) / self.tile_size) * self.tile_size,
                                       round((position[1] + self.tile_size - 8) / self.tile_size) * self.tile_size]
            case "up":
                self.build_position = [round(position[0] / self.tile_size) * self.tile_size,
                                       round((position[1] - self.tile_size * 2) / self.tile_size) * self.tile_size]
