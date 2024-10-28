import sys  #permet d'interagir avec le système d'exploitation, pour quitter proprement le programme
import pygame   #Importe la bibliothèque pygame
bonjour = 3
style = 1000
class Game:
    def __init__(self):
        pygame.init()
        #Initialisation des modules pygame, de la bibliothèque pygame

        pygame.display.set_caption('ninja game')
        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():    #À chaque itération de la boucle, cette ligne récupère tous les événements (comme les clics de souris ou les touches du clavier) qui se sont produits depuis le dernier cycle.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exist
                             
            pygame.display.update()
            self.clock.tick(60)
     
Game().run()
