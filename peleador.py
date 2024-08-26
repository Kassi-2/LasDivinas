import pygame

class Peleador():
    def __init__(self, x,y):
        self.rect= pygame.Rect((x,y,80,180))
        self.vida= 100

    def movimiento(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_d]:
            self.vida-=1

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla,(255,0,0), self.rect)