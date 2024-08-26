import pygame
from peleador import Peleador

pygame.init()

anchoPantalla= 960
largoPantalla= 540

pantalla= pygame.display.set_mode((anchoPantalla, largoPantalla))
pygame.display.set_caption("caca")

reloj= pygame.time.Clock()
fps= 60

amarillo= (255,255,0)
rojo= (255,0,0)

fondo= pygame.image.load("assets/socompa-pano.jpg").convert_alpha()

hector= pygame.image.load("assets/Hector-Osandon-scaled.jpg").convert_alpha()

def dibujarFondo():
    fondoEscalado= pygame.transform.scale(fondo,(anchoPantalla,largoPantalla))
    pantalla.blit(fondoEscalado, (0,0))

def dibujarVida(vida, x, y):
    radio= vida/100
    pygame.draw.rect(pantalla, rojo, (x,y, 400, 30))
    pygame.draw.rect(pantalla, amarillo, (x,y, 400 * radio, 30))

peleador1= Peleador(200,310)
peleador2= Peleador(700,310)

run= True

while run:

    reloj.tick(fps)

    dibujarFondo()

    peleador1.movimiento()
    peleador2.movimiento()

    dibujarVida(peleador1.vida, 20 ,20)
    dibujarVida(peleador2.vida, 540, 20)

    peleador1.dibujar(pantalla)
    peleador2.dibujar(pantalla)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run= False

    pygame.display.update()

pygame.quit()