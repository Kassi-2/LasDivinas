import pygame

class Peleador():
    def __init__(self, x,y, data, hoja, pasosAnimacion):
        self.tamaño= data[0]
        self.listaAnimacion= self.cargarImagenes(hoja, pasosAnimacion)
        self.rect= pygame.Rect((x,y,80,180))
        self.vida= 100

    def cargarImagenes(self, hoja, pasosAnimacion):
        listaAnimacion=[]
        for y, animacion in enumerate(pasosAnimacion):
            listaImgTemporal=[]
            for x in range(animacion):
                print(x)
                print(y)
                print(self.tamaño)
                imgTemporal= hoja.subsurface(x*self.tamaño, y*self.tamaño, self.tamaño, self.tamaño)    
                listaImgTemporal.append(imgTemporal)
            listaAnimacion.append(listaImgTemporal)
        print(listaAnimacion)
        return listaAnimacion

    def movimiento(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_d]:
            self.vida-=1

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla,(255,0,0), self.rect)
        #pantalla.blit(self.image, (self.rect.x,self.rect.y))