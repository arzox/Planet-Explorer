import pygame
import sys
import pytmx
from pytmx.util_pygame import load_pygame
import pyscroll
from pyscroll import PyscrollGroup
import abc
import random

pygame.init()
pygame.font.init()
pygame.mixer.pre_init()
pygame.display.init()

# Taille de l'écran
screen_size = (850, 640)
# Création de l'écran
screen = pygame.display.set_mode(screen_size)

push_buttons_colors = {
    'bottom': '#2e5cb8',
    'normal': '#4775d1',
    'hover': '#0099ff',
    'press': '#4db8ff'
}

#polices d'ecriture
default_font = pygame.font.Font(None, 30)
debug_font = pygame.font.SysFont("consolas", 20)
sans_font = pygame.font.SysFont("Comic Sans MS", 60)


def center_width(width: int, container: int):
    """
    Centre une largeur à partir d'une première largeur, et d'une largeur servant de conteneur.
    """
    return container // 2 - width // 2

def center_height(height: int, container: int):
    """
    Centre une hauteur à partir d'une première hauteur, et d'une hauteur servant de conteneur.
    """
    return container // 2 - height // 2

def center_rect(rect: pygame.Rect, container: pygame.Rect) -> (int, int):
    """
    Une fonction permettant de centrer une surface à l'intérieur d'une autre surface.
    Renvoie uniquement des coordonnées, ne modifie aucune des deux surfaces.
    """
    return (
        center_width(rect.width, container.width),
        center_height(rect.height, container.height)
    )

def center_surface(surface: pygame.Surface, container: pygame.Surface) -> (int, int):
    """
    Une fonction permettant de centrer une surface à l'intérieur d'une autre surface.
    Renvoie uniquement des coordonnées, ne modifie aucune des deux surfaces.
    """
    content_width, content_height = surface.get_size()
    container_width, container_height = container.get_size()
    return (
        center_width(content_width, container_width),
        center_height(content_height, container_height)
    )


class Button(pygame.sprite.Sprite):
    """
    Une classe représentant un bouton cliquable.
    Un bouton a un texte, une surface et un rectangle servant de boîte de collision.
    """

    def __init__(self, label: str, size: (int, int), position: (int, int), action: callable):
        """
        Initialise un nouveau bouton.
        Une fonction, méthode ou autre objet appelable est passée en paramètres et est appelé lors du click sur
        le bouton sans aucun paramètre.
        """
        super().__init__()

        # Données spécifiques au bouton (texte, action, souris au-dessus...).
        self.action: callable = action
        self.label = label
        self.hovering = False

        # Image du bouton (composant graphique).
        self.image = pygame.Surface(size)
        self.image.fill('#000000')
        self.render('#FFFFFF')

        # Rectangle du bouton (boîte de collision et d'affichage).
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def render(self, color: str):
        """
        Affiche le texte du bouton sur son image, au centre et avec une couleur indiquée (code hexadecimal).
        Cette action est gourmande en temps, il est donc conseillé de l'utiliser peut souvent.
        """
        # Créer une surface avec le texte de la couleur indiquée.
        text = debug_font.render(self.label, True, color, '#000000')
        # Affiche le texte sur l'image du bouton au centre.
        self.image.blit(
            text, center_surface(text, self.image)
        )

    def update(self, event: pygame.event.Event, contained: (int, int) = None):
        """
        Met à jour le bouton, active son action lorsque la souris clique dessus
        et change sa couleur si la souris est placée au-dessus du bouton.
        """

        rect = self.rect.copy()
        if contained is not None:
            rect.x += contained[0]
            rect.Y += contained[1]

        # Lorsque la pointe de la souris rentre en contact avec la boîte de collision.
        if rect.collidepoint(*pygame.mouse.get_pos()):

            # Si ce n'était pas le cas au par-avant.
            if self.hovering is False:
                # Change la couleur du texte du bouton.
                self.render('#FFFF00')
                # Indique qu'à présent la souris est au-dessus du bouton.
                self.hovering = True

            # Si le click gauche est actionné.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                # Actionne la fonction.
                self.action()

        # Si la souris n'est pas placée au-dessus du bouton, et que ce n'était pas le cas avant.
        elif self.hovering is True:
            # Change la couleur du texte du bouton.
            self.render('#FFFFFF')
            # Indique qu'à présent la souris n'est au-dessus du bouton.
            self.hovering = False


class PushButton(Button):
    """
    Classe représentant un bouton poussoir, qui fait une animation lorsqu'il est pressé, et ne s'active
    que lorsqu'il est relâché.
    Il est possible en plus de choisir sa couleur, le rayon de l'arrondissement des angles ainsi que l'élévation.
    """

    def __init__(
            self, label: str, size: (int, int), position: (int, int), action: callable,
            elevation: int = 8, border_radius: int = 16
    ):
        """
        Construit une nouvelle instance de la classe 'PushButton' représentant un bouton poussoir
        et héritant de la classe 'Button'.
        Le bouton poussoir fonctionne de la même manière qu'un bouton normal, à l'exception qu'il est animé
        et est activé lorsqu'il est relâché.
        """

        # Appel du constructeur de la superclasse 'Button'
        super().__init__(label, size, position, action)

        # Attributs primaires
        self.pressed = False
        self.elevation = elevation
        self.border_radius = border_radius

        # Taille
        self.size = list(size)
        # Image
        self.image = pygame.Surface((self.size[0], self.size[1] + self.elevation))
        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1] - self.elevation

        # Boîte de collision
        self.layer = self.image.get_rect()
        self.layer.height -= self.elevation
        # Texte
        self.text = default_font.render(self.label, True, '#FFFFFF')

        # Affiche le bouton.
        self.display(push_buttons_colors['normal'])

    def display(self, color: str):
        """
        Affiche le texte du bouton sur son image, au centre et avec une couleur indiquée (code hexadecimal).
        Cette action est gourmande en temps, il est donc conseillé de l'utiliser peut souvent.
        """
        # Filling with black.
        self.image.fill('#000000')
        # Drawing button's bottom part.
        pygame.draw.rect(
            self.image, push_buttons_colors['bottom'],
            pygame.Rect(0, self.elevation, *self.size),
            border_radius=self.border_radius
        )
        # Drawing button's top part and text.
        pygame.draw.rect(self.image, color, self.layer, border_radius=self.border_radius)
        x, y = center_rect(self.text.get_rect(), self.layer)
        y += self.layer.y
        self.image.blit(self.text, (x, y))

    def update(self, event: pygame.event.Event, contained: (int, int) = None):
        """
        Met à jour le bouton, active son action lorsque la souris clique dessus
        et change sa couleur si la souris est placée au-dessus du bouton.
        """

        rect = self.rect.copy()
        if contained is not None:
            rect.x += contained[0]
            rect.y += contained[1]

        # Lorsque la pointe de la souris rentre en contact avec la boîte de collision.
        if rect.collidepoint(*pygame.mouse.get_pos()):

            # Si ce n'était pas le cas au par-avant.
            if self.hovering is False:
                # Change la couleur du bouton.
                self.display(push_buttons_colors['hover'])
                # Indique qu'à présent la souris est au-dessus du bouton.
                self.hovering = True

            # Si le click gauche est actionné.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:

                # Si le bouton n'était pas en train d'être pressé.
                if self.pressed is False:
                    # Abaisse le bouton.
                    self.layer.y = self.elevation
                    # Change la couleur du bouton.
                    self.display(push_buttons_colors['press'])
                    # Indique que le bouton est à présent pressé.
                    self.pressed = True

                # Si le bouton était en train d'être pressé.
                else:
                    # Relève le bouton.
                    self.layer.y = 0
                    # Change la couleur du bouton.
                    self.display(push_buttons_colors['normal'])
                    # Indique que le bouton est relâché.
                    self.pressed = False

            elif self.pressed is True:
                # Indique que le bouton est relâché.
                self.pressed = False
                # Relève le bouton.
                self.layer.y = 0
                # Change la couleur du bouton.
                self.display(push_buttons_colors['normal'])
                # Actionne la fonction.
                self.action()

        # Si la souris n'est pas placée au-dessus du bouton, et que ce n'était pas le cas avant.
        elif self.hovering is True:
            # Change la couleur du bouton.
            self.display(push_buttons_colors['normal'])
            # Indique qu'à présent la souris n'est au-dessus du bouton.
            self.hovering = False