import pygame
import socket
from peleador import Peleador

#CONEXIOOOOON
server = '192.168.1.123' #IP del compu
port = 5050
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    c.connect((server, port))
    print("Conexión exitosa")
except socket.error:
    print("Error")
    exit()

jugadorId = c.recv(1024).decode('utf-8')
print(f"Entró el jugador {jugadorId}")


#JUEGOOOO

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
rojo= (255,0,170)

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

peleadores={0: Peleador(1, 200,310, samuraiData, samurai, samuraiPasosAnimacion, False),
 1: Peleador(2, 700,310, samuraiData, samurai, samuraiPasosAnimacion, True)} 

peleador1 = peleadores[int(jugadorId)]
peleador2= peleadores[1-int(jugadorId)]

run= True

while run:

    reloj.tick(fps)

    dibujarFondo()

    if cuentaInicio<=0:
        print(jugadorId)

        if jugadorId=="1":
          peleador1.move(anchoPantalla, largoPantalla, pantalla, peleador2, finRonda)
          dañoHecho=peleador1.dañoHecho
          posicion = f"{jugadorId}:{peleador1.rect.x},{peleador1.rect.y}:{peleador2.vida}:{dañoHecho}"
        elif jugadorId=="0":
           peleador2.move(anchoPantalla, largoPantalla, pantalla, peleador1, finRonda)
           dañoHecho=peleador2.dañoHecho
           posicion = f"{jugadorId}:{peleador2.rect.x},{peleador2.rect.y}:{peleador1.vida}:{dañoHecho}"
        
        c.send(posicion.encode())
        if jugadorId=="1":
           peleador1.dañoHecho=0
        elif jugadorId=="0":
           peleador2.dañoHecho=0
        try:
           data= c.recv(1024).decode('utf-8')
           if data:
              jugadorId2, coords, vidaJugador2, dañoRecibido= data.split(":")
              print(data)
              x, y = map(int, coords.split(","))
              vidaJugador2= int(vidaJugador2)
              dañoRecibido=int(dañoRecibido)
              if jugadorId2!=jugadorId:
                if jugadorId=="1":
                  peleador2.rect.x=x
                  peleador2.rect.y=y
                  peleador2.vida=vidaJugador2
                  peleador1.vida-=dañoRecibido
                elif jugadorId=="0":
                  peleador1.rect.x=x
                  peleador1.rect.y=y
                  peleador1.vida=vidaJugador2
                  peleador2.vida-=dañoRecibido
           else:
              print("Ya no hay server")
              break
        except Exception:
           print("Error")
           break
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

pygame.quit()
c.close()
