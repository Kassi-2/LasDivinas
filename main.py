import pygame
from fighter import Fighter
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fight")
imagen = pygame.image.load("background.png").convert_alpha()

def draw_bg():
  scaled_bg = pygame.transform.scale(imagen,(SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#set framerate
clock = pygame.time.Clock()
FPS = 60
fighter_1 = Fighter(1,200, 310, False)
fighter_2 = Fighter(2,700, 310, True)

run = True
while run:
  draw_bg()
  fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
  fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)

  fighter_1.draw(screen)
  fighter_2.draw(screen)
  clock.tick(FPS)
  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

#exit pygame
pygame.quit()