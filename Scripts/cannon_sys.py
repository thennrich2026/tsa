import pygame
import classes as c
import settings
import math
import gametimer

class Cannon_Ball(c.Sprite):
    cannon_projectiles = []
    def __init__(self, image, image_scale, speed, dmg, pierce):
        super().__init__(image, image_scale)
        self.speed = speed
        self.dmg = dmg
        self.pierce = pierce


    def get_velocity_angle(self, angle):
        return ( math.cos((angle - 90) * math.pi/180) * self.speed, math.sin((angle - 90) * math.pi/180) * self.speed )
    

cannon_dict = {
    'multishot' : {
        'multishot_1' : {
            'img' : settings.img_dict['multishot_1'],
            'pivot' : (10*2, 49*2),
            'firerate' : 750,
            'auto' : True,
            'dmg' : 5,
            'bullet_speed' : 10,
            'pierce' : 1,
            'projectiles' : 1,
            'next_evo' : 'multishot_2'
        },

        'multishot_2' : {
            'img' : settings.img_dict['multishot_2'],
            'pivot' : (12*2, 49*2),
            'firerate' : 500,
            'auto' : True,
            'dmg' : 5,
            'bullet_speed' : 14,
            'pierce' : 1,
            'projectiles' : 1,
            'next_evo' : 'multishot_3'
        },

        'multishot_3' : {
            'img' : settings.img_dict['multishot_3'],
            'pivot' : (12*2, 55*2),
            'firerate' : 250,
            'auto' : True,
            'dmg' : 5,
            'bullet_speed' : 18,
            'pierce' : 1,
            'projectiles' : 1,
            'next_evo' : 'MAXED'
        }
    },
    'sniper' : {
        'sniper_1' : {
            'img' : settings.img_dict['sniper_1'],
            'pivot' : (0, 0),
            'firerate' : 1000,
            'auto' : True,
            'dmg' : 1,
            'bullet_speed' : 15,
            'pierce' : 1,
            'projectiles' : 1,
            'next_evo' : 'sniper_2'
        },
        'sniper_2' : {
            'img' : settings.img_dict['sniper_2'],
            'pivot' : (0, 0),
            'firerate' : 100,
            'auto' : True,
            'dmg' : 1,
            'bullet_speed' : 1,
            'pierce' : 1,
            'projectiles' : 1,
            'next_evo' : 'sniper_3'
        },
        'sniper_3' : {
            'img' : settings.img_dict['sniper_3'],
            'pivot' : (0, 0),
            'firerate' : 100,
            'auto' : True,
            'dmg' : 1,
            'bullet_speed' : 1,
            'pierce' : 1,
            'projectiles' : 1,
            'next_evo' : 'MAXED'
        },
    }
}


class Cannon(c.Sprite):
    def __init__(self, cannon_type):
        
        super().__init__(cannon_type['img'], (cannon_type['img'].get_width()*2 , cannon_type['img'].get_height()*2 )) 
        self.original_image = self.image
        self.origin = (0,0)
        self.pivot = cannon_type['pivot']
        self.rect = self.image.get_rect(topleft = (self.origin[0] - self.pivot[0], self.origin[1] - self.pivot[1]))
        self.angle = 0
        self.pos = self.origin
        self.cannon_type = cannon_type
        if self.cannon_type['auto'] == True:
            self.timer = gametimer.Timer(self.cannon_type['firerate'])

    def tick(self, screen=settings.screen):
        
        if self.angle > 45:
            self.angle = 45
        elif self.angle < -45:
            self.angle = -45

        #--- Firing ---#
        if self.cannon_type['auto'] == True:
            if self.timer.check() == True:
                self.fire()
                self.timer.restart()
        else:
            pass

        #--- Anchor Rotate ---#
        image_rect = self.original_image.get_rect(topleft = (self.origin[0] - self.pivot[0], self.origin[1]-self.pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)
        rotated_image_center = (self.pos[0] - rotated_offset.x, self.pos[1] - rotated_offset.y)

        #--- Final Update---#
        self.image  = pygame.transform.rotate(self.original_image, self.angle)
        self.rect   = self.image.get_rect(center = rotated_image_center)
        screen.blit(self.image, self.rect)
        

    def fire(self):
        bullet = Cannon_Ball(settings.img_dict['bullet'], (12,12), self.cannon_type['bullet_speed'], self.cannon_type['dmg'], self.cannon_type['pierce'])
        coord = self.rect.center[0] - bullet.image.get_width()/2, self.rect.center[1] - bullet.image.get_height()/2
        bullet.x, bullet.y = coord
        vel = bullet.get_velocity_angle(-self.angle)
        bullet.vel_x = vel[0]
        bullet.vel_y = vel[1]

        Cannon_Ball.cannon_projectiles.append(bullet)