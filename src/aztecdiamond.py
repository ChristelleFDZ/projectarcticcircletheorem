import random
import numpy as np
import pygame

#option d'affichage (on pourra changer les parametres si trop petit a voir ensemble.. )
#definition des couleurs et orientation 
AFFICHAGE_Taille = 1000
ARRIEREPLAN_Couleur = (20, ) * 3 # Choix noirs ??
BORDURE_Couleur = (0, ) * 3
BORDURE_Largeur = 2
ORIENTATIONS = N, S, E, O = range(4) #direction
PAVAGE_Couleur = {
    N: (0, 114, 189) ,  # bleu
    S: (119, 172, 48) ,  # vert
    E: (162, 20, 47) ,  # rouge
    O: (237, 177, 32) ,  # jaune
    None: (200, ) * 3
}
PAVAGE_Etape = {
    N: np.array([-1, 0]), #Nord
    S: np.array([1, 0]), # Sud
    E: np.array([0, 1]), # Est
    O: np.array([0, -1]), #Ouest
}
PAVAGE_Etape_conflits = {
    N: S ,
    S: N ,
    E: O ,
    O: E ,
}

class aztecdiamond:
    def __init__(self, order, fps=4):
        assert type(order) is int and order > 0
        self.order = order
        self.fps = fps
        self.tiles = []

        self.diamond = None
        self.pavage = None
        self.generate_diamond_array()

        pygame.init()
        self.screen = pygame.display.set_mode([AFFICHAGE_Taille, AFFICHAGE_Taille])
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        self.clock = pygame.time.Clock()

        self.grille_rects = None
        self.generate_grille_rects()

    def generate_diamond_array(self):
        tri = np.triu(np.ones([self.order] * 2))
        self.diamond = np.concatenate([
            np.concatenate([np.flipud(tri), np.transpose(tri)], axis=1),
            np.concatenate([tri, np.fliplr(tri)], axis=1)
        ], axis=0)
        self.pavage = np.zeros([2 * self.order] * 2, dtype='O')
