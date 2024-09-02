import pygame
from peleador import Peleador

pygame.init()

anchoPantalla= 960
largoPantalla= 540

pantalla= pygame.display.set_mode((anchoPantalla, largoPantalla))
pygame.display.set_caption("caca")

reloj= pygame.time.Clock()
fps= 60

cuentaInicio=3
actualizarCuenta=pygame.time.get_ticks()
finRonda= False
finRondaEnfriamiento= 2000

amarillo= (255,255,0)
rojo= (255,0,0)

samuraiTamaño= 200
samuraiEscalado= 3.5
samuraiOffset= [90,70]
samuraiData= [samuraiTamaño, samuraiEscalado, samuraiOffset]

fondo= pygame.image.load("assets/socompa-pano.jpg").convert_alpha()
victoria= pygame.image.load("assets/victoria.png").convert_alpha()

hector= pygame.image.load("assets/Hector-Osandon-scaled.jpg").convert_alpha()
samurai= pygame.image.load("assets/samurai.png").convert_alpha()

font= pygame.font.Font("assets/Verve.ttf", 80)

samuraiPasosAnimacion=[6,6,6,2,8,2,8,4,4]

def dibujarCuentaInicio(texto, font, texto_col, x, y):
  img= font.render(texto, True, texto_col)
  pantalla.blit(img, (x,y))
    

def dibujarFondo():
    fondoEscalado= pygame.transform.scale(fondo,(anchoPantalla,largoPantalla))
    pantalla.blit(fondoEscalado, (0,0))

def dibujarVida(vida, x, y):
    radio= vida/100
    pygame.draw.rect(pantalla, rojo, (x,y, 400, 30))
    pygame.draw.rect(pantalla, amarillo, (x,y, 400 * radio, 30))

peleador1= Peleador(1, 200,310, samuraiData, samurai, samuraiPasosAnimacion, False)
peleador2= Peleador(2, 700,310, samuraiData, samurai, samuraiPasosAnimacion, True)

run= True

while run:

    reloj.tick(fps)

    dibujarFondo()

    if cuentaInicio<=0:
        peleador1.move(anchoPantalla, largoPantalla, pantalla, peleador2, finRonda)
        peleador2.move(anchoPantalla, largoPantalla, pantalla, peleador1, finRonda)
    else:
        dibujarCuentaInicio(str(cuentaInicio), font, rojo, anchoPantalla/2, largoPantalla/3)
        if(pygame.time.get_ticks()-actualizarCuenta)>=1000:
         cuentaInicio-=1
         actualizarCuenta= pygame.time.get_ticks()

    peleador1.actualizar()
    peleador2.actualizar()

    dibujarVida(peleador1.vida, 20 ,20)
    dibujarVida(peleador2.vida, 540, 20)

    peleador1.dibujar(pantalla)
    peleador2.dibujar(pantalla)

    if finRonda==False:
      if peleador1.vivo==False:
        finRonda=True
        rondaOverTime= pygame.time.get_ticks()
      elif peleador2.vivo==False:
        finRonda=True
        rondaOverTime= pygame.time.get_ticks()
    else:
      pantalla.blit(victoria, (280, 80))
      if pygame.time.get_ticks() - rondaOverTime>finRondaEnfriamiento:
        finRonda= False
        cuentaInicio=3
        peleador1= Peleador(1, 200,310, samuraiData, samurai, samuraiPasosAnimacion, False)
        peleador2= Peleador(2, 700,310, samuraiData, samurai, samuraiPasosAnimacion, True)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run= False

    pygame.display.update()
