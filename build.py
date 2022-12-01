import pygame
import pytmx
from building import Building


# Sprite qui contient les batiments
class BuildTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


# Sprite de la visualisation de construction
class BuildPreviewTile(pygame.sprite.Sprite):
    def __init__(self, surf, instance):
        super().__init__()

        # creation sprite
        self.image = surf
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(topleft=[0,0])

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
            self.image.fill((10,255,235))
        else:
            self.image.fill((255,0,0))


# class qui gere la construction
class Build:
    def __init__(self, tmx_data: pytmx.TiledMap, all_sprite):
        # recupere valeur de la carte
        self.tmx_data = tmx_data
        self.all_sprite = all_sprite
        self.tile_size = self.tmx_data.tileheight

        self.create_ground_grid()
        self.create_ground_rects()

        # creer la tile de previsualisation
        self.build_position = [0, 0]
        self.build_preview_tile = BuildPreviewTile(pygame.image.load(Building.HOLO.value), self)

    # creer une table de la carte avec les tiles de sol
    def create_ground_grid(self):
        map_height, map_width = self.tmx_data.height, self.tmx_data.width
        self.grid = [[[] for col in range(map_width)] for row in range(map_height)]
        for x, y, _ in self.tmx_data.get_layer_by_name("ground").tiles():
            self.grid[y][x].append('B')

    # creer une position pour les tiles en fonction de ou regarde le joueur
    def set_build_position(self, direction: str, position: list):
        match direction:
            case "right":
                self.build_position = [round((position[0] + self.tile_size * 3) / self.tile_size) * self.tile_size,
                                       round((position[1] + self.tile_size - 8) / self.tile_size) * self.tile_size]
            case "down":
                self.build_position = [round((position[0]) / self.tile_size) * self.tile_size, round((position[1] + self.tile_size * 3) / self.tile_size) * self.tile_size]
            case "left":
                self.build_position = [round((position[0] - self.tile_size * 2) / self.tile_size) * self.tile_size,
                                       round((position[1] + self.tile_size - 8) / self.tile_size) * self.tile_size]
            case "up":
                self.build_position = [round(position[0] / self.tile_size) * self.tile_size, round((position[1] - self.tile_size * 2) / self.tile_size) * self.tile_size]

    # convertie la table avec des lettres en table avec des rect
    def create_ground_rects(self):
        self.ground_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'B' in cell:
                    x = index_col * self.tile_size
                    y = index_row * self.tile_size
                    rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    self.ground_rects.append(rect)

    # verifie si le build est possible
    def check_buildable(self):
        for rect in self.ground_rects:
            if rect.collidepoint(self.build_position):
                x = self.build_position[0] // self.tile_size
                y = self.build_position[1] // self.tile_size

                if 'B' in self.grid[y][x] and not 'X' in self.grid[y][x]:
                    return True
        return False

    # fait apparaitre un batiment au coordonnees
    def set_build(self):
        for rect in self.ground_rects:
            if rect.collidepoint(self.build_position):
                x = self.build_position[0] // self.tile_size
                y = self.build_position[1] // self.tile_size

                if 'B' in self.grid[y][x] and not 'X' in self.grid[y][x]:
                    # fait apparaitre le sprite et empeche la creation d'un batiment au même endroit
                    self.grid[y][x].append('X')
                    sprite = BuildTile(pos=(x * self.tile_size, y * self.tile_size),
                                       surf=pygame.image.load(Building.HOLO.value))
                    self.all_sprite.add(sprite)

    # fait apparaitre la previsualisation
    def set_build_preview(self):
        self.all_sprite.add(self.build_preview_tile)
        self.build_preview_tile.is_preview = True

    # fait disparaitre la previsualisation
    def remove_build_preview(self):
        self.all_sprite.remove(self.build_preview_tile)
        self.build_preview_tile.is_preview = False
