"""
This program will set up the paving process and at the end it will return an Aztec diamond of order 70
The elaboration of the Diamond respects the paving process with dominoes : The square dance or crazy dance.
In fact, the execution of the program requires the use of the class Domino. It will use the pygame package a lot.
"""
# On importe les modules random, numpy, pygame et notre classe domino pour pouvoir les utiliser dans notre code
import random
import numpy as np
import pygame 
from domino import Domino


#definition des couleurs et orientation 
AFFICHAGE_Taille = 800 
ARRIEREPLAN_Couleur = (20, ) * 3 
BORDURE_Couleur = (0, ) * 3 
Bordure_Largeur = 2 
ORIENTATIONS = N, S, E, O = range(4)
PAVAGE_Couleur = { 
    N: (0, 114, 189),  # Bleu
    S: (119, 172, 48),  # vert
    E: (162, 20, 47),  # rouge
    O: (237, 177, 32),  # jaune 
    None: (200, ) * 3
}
PAVAGE_Etapes = { 
    N: np.array([-1, 0]),
    S: np.array([1, 0]),
    E: np.array([0, 1]),
    O: np.array([0, -1]),
}
PAVAGE_Etape_conflits = { 
    N: S,
    S: N,
    E: O,
    O: E,
}

class AztecDiamond:
    """
    This class will contain the different steps to create the Aztec diamond

    """

    def __init__(self, order, fps=4):
        """ 
        Creates the variables associated with the class AztecDiamond
        :type order: int 
        :param order: an instance of the class passed to __init__ . It represents the order of the Aztec Diamond
        :type fps: int
        :param fps: an instance of the classpassed to __init__ . The initial value of fps is 4

        Uses pygame.init() to initialise all of the pygame modules. Without this the modules would not work
        The WIDTH and HEIGHT constants are used to create a window, which would have a width of 800 pixels 
            and a height of 800 pixels. The function used in SCREEN, pygame.display.set_mode((AFFICHAGE_Taille, AFFICHAGE_Taille)), 
            will set the mode of the display and return a Surface object. Note how the parameters for this 
            function are the WIDTH and HEIGHT constants defined earlier.

        """
        assert type(order) is int and order > 0
        self.order = order
        self.fps = fps
        self.tiles = []

        self.diamond = None
        self.pavage = None
        self.generate_diamond_array()

        pygame.init() # initialise le module pygame 
        self.screen = pygame.display.set_mode([AFFICHAGE_Taille, AFFICHAGE_Taille])
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        self.clock = pygame.time.Clock()

        self.grille_rects = None
        self.production_rect_grille()

    def generate_diamond_array(self):
        """
        Generates diamond array 
        """
        tri = np.triu(np.ones([self.order] * 2))
        self.diamond = np.concatenate([
            np.concatenate([np.flipud(tri), np.transpose(tri)], axis=1),
            np.concatenate([tri, np.fliplr(tri)], axis=1)
        ], axis=0)
        
        self.pavage = np.zeros([2 * self.order] * 2, dtype='O')

# Cette fonction g??n??re une grille avec des r??ctangles pour la production du diamant
    def production_rect_grille(self):
        """
        Generates a grid with rectangles
        Uses pygame object for storing rectangular coordinates :pygame.Rect
        """
        self.grille_rects = [
            pygame.Rect(
                round(AFFICHAGE_Taille / 2 * (i + 1) / (self.order + 1)),  # gauche
                round(AFFICHAGE_Taille / 2 * (1 - (i + 1) / (self.order + 1))),  # en haut
                round(AFFICHAGE_Taille * (self.order - i) / (self.order + 1)),  # largeur
                round(AFFICHAGE_Taille * (i + 1) / (self.order + 1)),  # taille
            )
            for i in range(self.order)
        ]
        
# Description des ??tapes du pavage
    def etape_pavage(self, draw: bool = False):
        """
        Describes the paving process by following the crazy dance or square dance or the iterating shuffling.
        There are 4 different steps: first, the increase of the Diamond size, then, the 
        removal of opposing tiles,followed by te moving tiles and finally,the filling by two dominoes. 
        This function uses 4 different functions : augmentation_taille, suppression_oppose, draw, remplissage_deuxdeux

        :type draw: bool
        :param order: the default value of draw is False
        """
        self.augmentation_taille()  #test--self.order
        if draw:
            self.draw()
        self.suppression_oppose() # supprimer les carreaux 
                                        #orient??s dans le m??me sens
        if draw:
            self.draw()
        self.move_tiles()
        if draw:
            self.draw()
        self.remplissage_deuxdeux() # remplir 2 par 2 
        if draw:
            self.draw()
# 
    def augmentation_taille(self): 
        """
        Increases the size of the Diamond
        At each iteration, the order increases by one
        """
        self.order += 1

        pavage = self.pavage
        self.generate_diamond_array()  #  pavage 
        self.pavage[1:-1, 1:-1] = pavage

        self.production_rect_grille()
        [tile.gen_rect(order=self.order) for tile in self.tiles]
        

    def suppression_oppose(self):
        """
        Removes tiles with opposite directions or orientations
        """

        for i, j in zip(*np.where(self.diamond)):
            tile = self.pavage[i, j]
            if tile == 0:
                continue
            i2, j2 = np.array([i, j]) + PAVAGE_Etapes[tile.orientation]
            if not (0 <= i2 <= 2 * self.order and 0 <= j2 <= 2 * self.order):
                continue
            tile2 = self.pavage[i2, j2]
            if tile2 == 0:
                continue
            if tile2.orientation == PAVAGE_Etape_conflits[tile.orientation]:
                self.pavage[np.where(self.pavage == tile)] = 0
                self.pavage[np.where(self.pavage == tile2)] = 0
                self.tiles.remove(tile)
                self.tiles.remove(tile2)



    def move_tiles(self):
        """
        Moves tiles in the right direction from the center to the corners
        """
        self.pavage = np.zeros([2 * self.order] * 2, dtype='O')
        for tile in self.tiles:
            tile.step()
            tile.gen_rect(order=self.order)
            self.pavage[tuple(tile.angle_droit_h + self.order)] = tile
            self.pavage[tuple(tile.angle_droit_h + self.order
                              + (PAVAGE_Etapes[S] if tile.orientation in (E, O) else PAVAGE_Etapes[E])
                              )] = tile
        
            
    def remplissage_deuxdeux(self):
        """
        Fills the Aztecdiamond(n=order) with a randomly-oriented pairs of dominoes.
        They can be oriented either East and West or North and South
        """
        while np.any((self.pavage == 0) & (self.diamond == 1)):
            ii, jj = [i[0] for i in np.where((self.pavage == 0) & (self.diamond == 1))]
            if random.random() < 0.5:
                #Haut/Bas
                tile_a = Domino((ii - self.order, jj - self.order), O, self.order)
                self.pavage[ii, jj] = tile_a
                self.pavage[ii + 1, jj] = tile_a
                tile_b = Domino((ii - self.order, jj - self.order + 1), E, self.order)
                self.pavage[ii, jj + 1] = tile_b
                self.pavage[ii + 1, jj + 1] = tile_b
            else:
                #Gauche/Droite
                tile_a = Domino((ii - self.order, jj - self.order), N, self.order)
                self.pavage[ii, jj] = tile_a
                self.pavage[ii, jj + 1] = tile_a
                tile_b = Domino((ii - self.order + 1, jj - self.order), S, self.order)
                self.pavage[ii + 1, jj] = tile_b
                self.pavage[ii + 1, jj + 1] = tile_b
            self.tiles.append(tile_a)
            self.tiles.append(tile_b)


    def draw(self):
        """
        This function allows you to create the animation thanks to the package pygame and 5 functions:
        gerer_evenements, ecran_vide,  dessin_grille, dessin_tuiles and dessin_commentaire
        Uses the pygame module to control the display window and screen : pygame.display.flip. In fact,
                This basically makes everything we have drawn on the screen Surface become visible and 
                updates the contents of the entire display. Without this line, the user wouldn't see 
                anything on their pygame screen.
        """
        self.gerer_evenements() 
        self.ecran_vide()
        self.dessin_grille()
        self.dessin_tuiles()
        self.dessin_commentaire()
        pygame.display.flip()

    def gerer_evenements(self):
        """
        Manages events thanks to the package pygame
        Uses the pygame module for monitoring time
        Gets the time in milliseconds thanks to clock.tic
        Gets the events from the queue thanks to pygame.event.get
        uninitializes all pygame modules thanks to pygame.quit: in fact This will make it so 
                            that when the user presses the exit button in the top corner, the 
                            event with the type pygame.QUIT occurs
        """
        if self.fps is not None:
            self.clock.tick(self.fps)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit() #uninitializes all pygame modules
                quit()

    def ecran_vide(self):
        """ 
        Fills the screen with the color of the background (black color)
        """
        self.screen.fill(ARRIEREPLAN_Couleur)


    def dessin_grille(self):
        """
        Draws grids thanks to the pygame package
        Uses pygame module for drawing rectangular shape : pygame.draw.rect()
        Uses pygame module to draw a straight line : pygame.draw.line()
        """
    
        [
            pygame.draw.rect(self.screen, rect=rect, color=PAVAGE_Couleur[None]) 
            for rect in self.grille_rects
        ]
        pygame.draw.line(
            self.screen,
            color=BORDURE_Couleur,
            start_pos=(round(AFFICHAGE_Taille / 2 / (self.order + 1)), round(AFFICHAGE_Taille / 2)),
            end_pos=(round(AFFICHAGE_Taille / 2 * (1 + self.order / (self.order + 1))), round(AFFICHAGE_Taille / 2)),
            width=Bordure_Largeur if self.order < 90 else 1
        )
        pygame.draw.line(
            self.screen,
            color=BORDURE_Couleur,
            start_pos=(round(AFFICHAGE_Taille / 2), round(AFFICHAGE_Taille / 2 / (self.order + 1))),
            end_pos=(round(AFFICHAGE_Taille / 2), round(AFFICHAGE_Taille / 2 * (1 + self.order / (self.order + 1)))),
            width=Bordure_Largeur if self.order < 90 else 1
        )
        [
            pygame.draw.rect(self.screen, rect=rect, color=BORDURE_Couleur, width=Bordure_Largeur if self.order < 90 else 1)
            for rect in self.grille_rects
        ]
        
    def dessin_tuiles(self):
        """
        This function draws tiles : the shape is rectangular and the color can be blue, red ,yellow or green accroding to the place and the direction of the tile
        Uses pygame module for drawing rectangular shape and add a color : pygame.draw.rect()
        """
        for tile in self.tiles:
            pygame.draw.rect(self.screen, rect=tile.rect, color=PAVAGE_Couleur[tile.orientation])
            pygame.draw.rect(self.screen, rect=tile.rect,
                             color=BORDURE_Couleur, width=Bordure_Largeur if self.order < 90 else 1)

    def dessin_commentaire(self):
        """
        Allows you to display comments in the visualization more precisely the title AztecDiamond
        """

        label = self.font.render(f'AztecDiamond (n = {self.order})', True, PAVAGE_Couleur[None])
        self.screen.blit(label, np.array([AFFICHAGE_Taille, 0]).astype(int) + [-label.get_width(), 0])

