"""
This file contains classes
"""

import pygame
import settings

class Sprite:
    active_sprites = []
    def __init__(self, image, image_scale):
        #creates the sprite's image and rect
        
        self.image_scale = image_scale
        self.image = pygame.transform.scale(image, (self.image_scale))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0
        
        #adds the sprite to a list of active sprites
        Sprite.active_sprites.append(self)
    
    #blits the sprite onto the chosen surface
    def update(self,screen=settings.screen):
        if not(settings.pausemomentum): 
            self.x += self.vel_x
            self.y += self.vel_y

        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def tick(self):
        self.update()
    
    #sets the sprites image to a new image
    def set_img(self,image):
        self.image = pygame.transform.scale(image, (self.image_scale))
    
    
    #deletes the sprite from memory
    def kill(self):
        Sprite.active_sprites.remove(self)
        del self

    def getSpriteCenterXY(self):
        return self.x+self.image_scale[0]/2,self.y+self.image_scale[1]/2




class Platform(Sprite):
    platform_list = []
    def __init__(self,image,image_scale, cannon, coord):
        Sprite.__init__(self,image,image_scale)
        self.cannon = cannon
        self.x = coord[0]
        self.y = coord[1]
        self.rect.x = coord[0]
        self.rect.y = coord[1]

        Platform.platform_list.append(self)

    def tick(self):
        self.update()

    def set_cannon_pos(self):
        coord = self.rect.midtop
        x = coord[0]-3
        y = coord[1]-20
        self.cannon.origin = (x,y)
        self.cannon.pos = (x,y)


class Health_Bar(Sprite):
    def __init__(self, color, empty_color,size:tuple,atached_sprite,x_offset,y_offset):
        Sprite.active_sprites.append(self)
        self.atached = atached_sprite
        self.color = color
        self.empty_color = empty_color
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.size = size
        self.rect = pygame.Rect(self.atached.rect.x+self.x_offset,self.atached.rect.y+self.y_offset,size[0],size[1])
        self.hpleft = 1

    def tick(self):
        self.rect.centerx = self.atached.rect.centerx+self.x_offset
        self.rect.centery = self.atached.rect.centery+self.y_offset
        pygame.draw.rect(settings.screen,self.empty_color,(self.atached.rect.x+self.x_offset,self.atached.rect.y+self.y_offset,self.size[0],self.size[1]))
        pygame.draw.rect(settings.screen,self.color,(self.atached.rect.x+self.x_offset,self.atached.rect.y+self.y_offset,self.size[0]*self.hpleft,self.size[1]))
    def hpcheck(self):
        self.hpleft = self.atached.hp/self.atached.maxhp