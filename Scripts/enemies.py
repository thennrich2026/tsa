"""
class system for enemies later? just writing a basic outline
so dont use this code. This is just to show the idea mainly"""
#imports

import pygame
from classes import *
import settings
import random
import gametimer as tm
import math
import random as r
from regenerator import *
#loaded for this area.


#enemy arrays

enemylist = {
    "basic" : {
        "weak" : {
            "hp": 10,
            "speed" : 5.0,
            "damage": 1,
            "image" : "basic",
            "image_scale" : (40*1.2,40*1.2)

        },
    },
    "diver" : {
        "weak" : {
            "hp": 5,
            "speed" : 5,
            "damage": 1,
            "image" : "diver",
            "image_scale" : (32*1.2,32*1.2)

        },
    },
    "error": {
        "Etype":{
            "hp": 1,
            "speed" : 5.0,
            "damage": 1,
            "image" : "error",
            "image_scale" : (100,100)
        },
        "E_error":{
            "hp": 1,
            "speed" : 5.0,
            "damage": 1,
            "image" : "error",
            "image_scale" : (100,100)
        }
    }
}

def init_enemy(type,variant): #this requires the above enemy list item
    es = enemylist[type][variant] #enemy stats, abrivated for simplicty
    try:
        if type == "basic":
            return Enemy(es["hp"],es["speed"],es["damage"],es["image"],es["image_scale"],type,variant)
        elif type == "diver":
            return Diver(es["hp"],es["speed"],es["damage"],es["image"],es["image_scale"],type,variant)
        else:
            #print("Unknown enemy type")
            es = enemylist["error"]["Etype"]
            return Enemy(es["hp"],es["speed"],es["damage"],es["image"],es["image_scale"],type,variant)
    except:
        #print("Undefined enemy error!!")
        es = enemylist["error"]["E_error"]
        return Enemy(es["hp"],es["speed"],es["damage"],es["image"],es["image_scale"],type,variant)





class Enemy(Sprite):
    enemy_list = []
    def __init__(self,hp: int,speed: float, damage:int,image, image_scale: tuple,type:str,variant:str):
        super().__init__(settings.img_dict[image],image_scale)
        self.hp = hp
        self.maxhp = hp
        self.speed = speed
        self.damage = damage
        self.vel_x = 0
        self.vel_y = 0
        self.state = "alive" #"dead","atacking"
        self.type = type
        self.variant = variant
        Enemy.enemy_list.append(self)
        
        
    def tick(self):
        self.movement()
        self.update()
    
    def movement(self):
        if self.rect.left <= settings.enemy_bounce_x:
            self.y += 20
            self.vel_x = self.speed
        elif self.rect.right >= settings.width - settings.enemy_bounce_x:
            self.y += 20
            self.vel_x = -self.speed
    
    def spawn(self,x,y,xy):
        self.x, self.y = x, y
        x += self.image_scale[0]
        if x > settings.width - self.image_scale[0] - settings.enemy_bounce_x:
            y += self.image_scale[1]
            x = xy[0]
        return x,y
    
    def onhit(self, projectile):
        self.hp -= projectile.dmg
        if self.hp <= 0:
            self.death()
            pass

    def death(self):
        self.enemy_list.remove(self)
        self.kill()

class Diver(Enemy):
    minimum_bounce = 4 #multiplier of bounce
    dive_height = 600 #how far before they dive towards regenerator
    def __init__(self,hp: int,speed: float, damage:int,image, image_scale: tuple,type:str,variant:str):
        Enemy.__init__(self,hp,speed, damage,image, image_scale,type,variant)
        self.drop_y = 900
        self.xy = (0,0)
        self.dive = True
        #self.target = pygame.Rect(0,0,20,20)
    
    def spawn(self,x,y,xy):
        self.x,self.y = x,y
        self.drop_y = y+self.image_scale[1]*4
        if x > (settings.width/2):
            x = xy[0]
            #print("left")
            y+=self.image_scale[1]
        elif x < (settings.width/2):
            x = settings.width-xy[0]
            #print("right")
        else:
            x = xy[0]
        return x,y
    
    def movement(self):
        if self.y >= Diver.dive_height and self.dive :
            self.dive = False
            rxy = Regenerator.active_regenerator.getSpriteCenterXY()
            self.set_velocity(rxy[0],rxy[1])
            #print("DIVE!")
        elif self.dive:
            if self.rect.left <= settings.enemy_bounce_x:
                target_x = r.randint((settings.enemy_bounce_x * Diver.minimum_bounce), (settings.width - (settings.enemy_bounce_x * Diver.minimum_bounce)))
                self.set_velocity(target_x,self.drop_y)
                #print(self.xy)
                #print("left side")
            
            elif self.rect.right >= settings.width - settings.enemy_bounce_x:
                self.drop_y += self.image_scale[1]
                target_x = r.randint((settings.enemy_bounce_x * Diver.minimum_bounce), (settings.width - (settings.enemy_bounce_x * Diver.minimum_bounce)))
                self.set_velocity(target_x, self.drop_y)
                #print(self.xy)
                #print("right side")
            
            elif self.rect.bottom >= self.drop_y:
                #print(self.vel_x)
                if self.vel_x > 0:
                    #print("ping")
                    self.set_velocity((settings.width - settings.enemy_bounce_x * 2), self.y-self.image_scale[1] * 4)
                elif self.vel_x < 0:
                    #print("pong")
                    self.set_velocity(settings.enemy_bounce_x * 2, self.y-self.image_scale[1] * 4)
                #print(self.xy)
                #print("middle")
        #pygame.draw.rect(settings.screen,"red",self.target)
        self.vel_x = self.xy[0]
        self.vel_y = -self.xy[1]
    
    def get_angle(xy:tuple,xy2:tuple):
        angle = math.degrees(math.atan2((xy2[0]-xy[0]),(xy2[1]-xy[1])))
        if angle < 0:
            angle+=360
        return angle
    
    def get_velocity_angle(self, angle):
        return ( math.cos((angle - 90) * math.pi/180) * self.speed, math.sin((angle - 90) * math.pi/180) * self.speed )
    
    def set_velocity(self,target_x,target_y):
        self.xy = self.get_velocity_angle(Diver.get_angle((self.x,self.y),(target_x,target_y)))
        #self.target.centerx = target_x
        #self.target.centery = target_y
        
