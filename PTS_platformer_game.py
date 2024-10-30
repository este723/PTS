import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()    #Récupère les dimenssions de l'écran
WIDTH, HEIGHT = info.current_w, info.current_h    #Renvoie les valeurs de l'écran à un instant t (d'où l'utilité lorsqu'on rafraichit l'écran)
window = pygame.display.set_mode((WIDTH - 10, HEIGHT - 50), pygame.RESIZABLE)


pygame.display.set_caption("Platformer")

BG_COLOR = (255, 255, 255)
FPS = 60
PLAYER_VEL = 5



def main(window):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #window.fill(BG_COLOR)
        pygame.display.flip()   #Mettre à jour l'affichage
    pygame.quit()
    # quit() ou sys.exit() (INUTILE)
    
if __name__ == "__main__":
    main(window) 