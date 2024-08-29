import pygame

class Peleador():
    def __init__(self, x,y, data, hoja, pasosAnimacion):
        self.tamaño= data[0]
        self.imagenEscalada= data[1]
        self.offset= data[2]
        self.listaAnimacion= self.cargarImagenes(hoja, pasosAnimacion)
        self.accion= 4#0:ataque1 #1:ataque2 #2:muerte #3:caida #4:inactivo #5:saltar #6:correr #7:golpeado #8:golpeado2
        self.indiceFrame=0
        self.imagen= self.listaAnimacion[self.accion][self.indiceFrame]
        self.tiempoActualizacion= pygame.time.get_ticks()
        self.rect= pygame.Rect((x,y,80,180))
        self.correr= False
        self.saltar= False
        self.atacar=False
        self.tipoAtaque=0
        self.enfriamientoAtaque=0
        self.golpe= False
        self.vida= 100
        self.vivo= True

    def cargarImagenes(self, hoja, pasosAnimacion):
        listaAnimacion=[]
        for y, animacion in enumerate(pasosAnimacion):
            listaImgTemporal=[]
            for x in range(animacion):
                imgTemporal= hoja.subsurface(x*self.tamaño, y*self.tamaño, self.tamaño, self.tamaño) 
                listaImgTemporal.append(pygame.transform.scale(imgTemporal, (self.tamaño*self.imagenEscalada, self.tamaño*self.imagenEscalada)))
            listaAnimacion.append(listaImgTemporal)
        return listaAnimacion

    def movimiento(self):
        self.correr=False
        self.tipoAtaque=0
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_d]:
            self.vida-=1
        if tecla[pygame.K_a]:
            self.correr= True

        if self.enfriamientoAtaque>0:
            self.enfriamientoAtaque-=1

    def actualizar(self):
        if self.vida<=0:
            self.vida=0
            self.vivo= False
            self.actualizarAccion(2)
        elif self.golpe== True:
            self.actualizarAccion(7)
        elif self.atacar==True:
            if self.tipoAtaque==1:
                self.actualizar(0)
            elif self.tipoAtaque==2:
                self.actualizar(1)
        elif self.saltar==True:
            self.actualizar(5)
        elif self.correr==True:
            self.actualizarAccion(6)
        else:
            self.actualizarAccion(4)
        enfriamientoAnimacion= 100
        self.imagen= self.listaAnimacion[self.accion][self.indiceFrame]
        if pygame.time.get_ticks()-self.tiempoActualizacion>enfriamientoAnimacion:
            self.indiceFrame+=1
            self.tiempoActualizacion= pygame.time.get_ticks()
        if self.indiceFrame>=len(self.listaAnimacion[self.accion]):
            if self.vivo==False:
                self.indiceFrame= len(self.listaAnimacion[self.accion]) - 1
            else:
                self.indiceFrame= 0
                if self.accion==3 or self.accion==4:
                    self.atacar= False
                    self.enfriamientoAtaque=50
                if self.accion==5:
                    self.hit=False
                    self.atacar=False
                    self.enfriamientoAtaque=20

    def actualizarAccion(self, nuevaAccion):
        if nuevaAccion!=self.accion:
            self.accion=nuevaAccion
            self.indiceFrame=0
            self.tiempoActualizacion= pygame.time.get_ticks()

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla,(255,0,0), self.rect)
        pantalla.blit(self.imagen, (self.rect.x-(self.offset[0]*self.imagenEscalada),self.rect.y-(self.offset[1]*self.imagenEscalada)))