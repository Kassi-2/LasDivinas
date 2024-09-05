import pygame

class Peleador():
    def __init__(self, jugador, x,y, data, hoja, pasosAnimacion, flip):
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
        self.dañoHecho=0
        self.vida= 100
        self.vivo= True
        self.vel_y= 0
        self.player = jugador
        self.flip = flip
    
    def __repr__(self):
        # Obtener el nombre de la clase
        class_name = self.__class__.__name__
        # Obtener los atributos de la clase
        attributes = ', '.join([f'{attr}={getattr(self, attr)!r}' for attr in self.__dict__])
        return f"{attributes}"


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
            

    def move(self, screen_width, screen_height, surface, target, finRonda):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.correr = False
        self.tipoAtaque = 0

        #get keypresses
        key = pygame.key.get_pressed()

      #check player 1 controls
        if self.atacar == False and self.vivo==True and finRonda==False:
            if self.player == 1:
             #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.correr = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.correr = True
                #jump
                if key[pygame.K_w] and self.saltar == False:
                    self.vel_y = -30
                    self.saltar = True
                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface,target)
                #determine which attack type was used
                if key[pygame.K_r]:
                    self.tipoAtaque = 1
                if key[pygame.K_t]:
                    self.tipoAtaque = 2

            #check player 2 controls
            if self.player == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.correr = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.correr = True
                #jump
                if key[pygame.K_UP] and self.saltar == False:
                    self.vel_y = -30
                    self.saltar = True
                if key[pygame.K_SPACE] or key[pygame.K_m]:
                    self.attack(surface, target)
                #determine which attack type was used
                if key[pygame.K_SPACE]:
                    self.tipoAtaque = 1
                if key[pygame.K_m]:
                    self.tipoAtaque = 2
            
        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.saltar = False
            dy = screen_height - 110 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
    
        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        self.atacar= True
        print(target)
        if attacking_rect.colliderect(target.rect):
            print("AUCH!")
            #target.golpe =True
            target.vida -=10
            print("-10")
            self.dañoHecho = 10
        #pygame.draw.rect(surface, (0,255,0), attacking_rect)

    def actualizar(self):
        if self.vida<=0:
            self.vida=0
            self.vivo= False
            self.actualizarAccion(2)
        elif self.golpe== True:
            self.actualizarAccion(7)
        elif self.atacar==True:
            if self.tipoAtaque==1:
                self.actualizarAccion(0)
            elif self.tipoAtaque==2:
                self.actualizarAccion(1)
        elif self.saltar==True:
            self.actualizarAccion(5)
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
                if self.accion==0 or self.accion==1:
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
        img= pygame.transform.flip(self.imagen, self.flip, False)
       # pygame.draw.rect(pantalla,(255,0,0), self.rect)
        pantalla.blit(img, (self.rect.x-(self.offset[0]*self.imagenEscalada),self.rect.y-(self.offset[1]*self.imagenEscalada)))