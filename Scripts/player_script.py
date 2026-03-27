import pygame
import classes as c
import settings


class Player_class(c.Sprite):
    def __init__(self, image, image_scale, hp):
        c.Sprite.__init__(self,image,image_scale)
        self.hp = hp
        self.player_grav = .5
        self.can_jump = True
        self.platform_collided = False
        self.rotate_cannon_left = False
        self.rotate_cannon_right = False
        self.dead = False

    def player_input(self, keys_press):
        if self.dead == False:
            if keys_press[pygame.K_d]:
                self.vel_x = 5
                self.set_img(settings.img_dict["player_left"]) 

            if keys_press[pygame.K_a]:
                self.vel_x = -5
                self.set_img(settings.img_dict["player_right"])

            elif not (keys_press[pygame.K_d] or keys_press[pygame.K_a]):
                self.set_img(settings.img_dict["player_stand"])
                self.vel_x = 0

            if keys_press[pygame.K_w]:
                if self.can_jump == True:
                    self.set_img(settings.img_dict["player_jump"])
                    self.vel_y = -10
                    self.can_jump = False

            if keys_press[pygame.K_LEFT]:
                self.rotate_cannon_left = True

            elif keys_press[pygame.K_RIGHT]:
                self.rotate_cannon_right = True

    def p_update(self, platform_list, screen = settings.screen):
        if self.dead == False:
            dx=0
            dy=0
            
            self.vel_y += self.player_grav
            
            if self.vel_y > 20:
                self.vel_y = 20

            if self.y > 1000:
                self.x = 450 -27
                self.y = 450 -27.2
            
            dx += self.vel_x
            dy += self.vel_y
            
            #NEVER TOUCH, BARELY WORKS
            for platform in platform_list:
                degree =0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    if self.vel_y >= 0:
                        dy = platform.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.can_jump = True
                        self.platform_collided = True
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y-1, self.rect.width, self.rect.height):
                    dx = 0
                    self.platform_collided = True
                
                if self.platform_collided == True:
                    if self.rotate_cannon_left == True:
                        degree = 1
                    if self.rotate_cannon_right == True:
                        degree = -1
                    if platform.cannon != 0:
                        platform.cannon.angle += degree*5
                    
            

                
                self.platform_collided = False
            
            self.x += dx
            self.y += dy


            self.rotate_cannon_left = False
            self.rotate_cannon_right = False
            self.platform_collided = False

            self.rect.topleft = (self.x, self.y)
            screen.blit(self.image, self.rect)