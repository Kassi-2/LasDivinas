import pygame

class Fighter():
    def __init__(self,player, x, y, flip):
        self.rect= pygame.Rect(x,y,80,180)
        self.vel_y= 0
        self.jump = False
        self.player = player
        self.attacking = False
        self.attack_type = 0
        self.flip = flip
        self.health= 100
    
    def draw(self, surface):
       pygame.draw.rect(surface, (255,0,0), self.rect)


    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #get keypresses
        key = pygame.key.get_pressed()

      #check player 1 controls
        if self.attacking == False:
            if self.player == 1:
             #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface,target)
                #determine which attack type was used
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

            #check player 2 controls
            if self.player == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_SPACE] or key[pygame.K_m]:
                    self.attack(surface, target)
                #determine which attack type was used
                if key[pygame.K_SPACE]:
                    self.attack_type = 1
                if key[pygame.K_m]:
                    self.attack_type = 2
            
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
            self.jump = False
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
        if attacking_rect.colliderect(target.rect):
            print("AUCH!")
            target.hit =True
            target.health -=10
            print("-10")
        pygame.draw.rect(surface, (0,255,0), attacking_rect)