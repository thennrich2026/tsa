from regenerator import Regenerator
import sys, pygame, os, random, cannon_sys

pygame.init()

#imports
import enemies as e, classes as c, random, player_script
from settings import *
from levels import *

#screen setup
bg = img_dict["space_bg"]
bg = pygame.transform.scale(bg, (900,900)) 
bg_rect = bg.get_rect(center=(450,450)) 

#-- Center Platform and Cannon --#
c_cannon = cannon_sys.Cannon(cannon_sys.cannon_dict['multishot']['multishot_3'], (25*2, 59*2), (0,0), (25,100))
center_platform = c.Platform(img_dict["center_platform"], (310,40), c_cannon, (295, 750))
center_platform.set_cannon_pos()
c_base = c.Sprite(img_dict['cannon_base'], (57*2, 10*2))
c_base.x = center_platform.rect.midtop[0] - 57
c_base.y = center_platform.rect.midtop[1] - c_base.image_scale[1]

#-- Left Platform and Cannon --#
l_cannon = cannon_sys.Cannon(cannon_sys.cannon_dict['multishot']['multishot_3'], (25*2, 59*2), (0,0), (25,100))
left_platform = c.Platform(img_dict["small_platform"], (210,40), l_cannon, (50,800))
left_platform.set_cannon_pos()
l_base = c.Sprite(img_dict['cannon_base'], (57*2, 10*2))
l_base.x = left_platform.rect.midtop[0] - 58
l_base.y = left_platform.rect.midtop[1] - c_base.image_scale[1]

#-- Right Platform and Cannon --#
r_cannon = cannon_sys.Cannon(cannon_sys.cannon_dict['multishot']['multishot_3'], (25*2, 59*2), (0,0), (25,100))
right_platform = c.Platform(img_dict["small_platform"], (210,40), r_cannon, (650,800))
right_platform.set_cannon_pos()
r_base = c.Sprite(img_dict['cannon_base'], (57*2, 10*2))
r_base.x = right_platform.rect.midtop[0] - 58
r_base.y = right_platform.rect.midtop[1] - c_base.image_scale[1]


cannons = [center_platform.cannon, c_base,  left_platform.cannon, l_base, right_platform.cannon, r_base]

# Player setup
player = player_script.Player_class(img_dict["player_stand"], (27*2, 50*2), 50)
player.x = 450
player.y = 450


clock = pygame.time.Clock()

#pre instanced code
level1 = Level( ["basic", "valkery", "valkery"], 1000)
level1.start()
player_hp_bar = Health_Bar("Green","Red",(60,10),player,0,-50)

# regenerator setup
regenerator = Regenerator(img_dict["regenerator_1"], (67,34),25,5000)
regenerator.x,regenerator.y = 450-67/2, 850-34/2

class State_manager():
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

    def get_state(self, new_state):
        self.current_state = new_state

class Scene():
    def __init__(self, display, state_manager):
        self.display = display
        self.game_state_manager = state_manager

    def run(self):
        pass

class Menu(Scene):
    def __init__(self, display, state_manager):
        Scene.__init__(self, display, state_manager)

    def run(self):
        pass

class Main(Scene):
    def __init__(self, display, state_manager):
        Scene.__init__(display, state_manager)

    def run(self):
        pass

state_manager = State_manager('menu')
menu = Menu(screen, state_manager)
main = Main(screen, state_manager)

states = {
    'menu' : menu,
    'main' : main
}
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Game Loop
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
while running:
    screen.blit(bg, bg_rect)
    
    #--------------------- Logic ---------------------#
    
    #Player logic
    keys = pygame.key.get_pressed()
    player.player_input(keys)
    
    if Level.active_level != None:
        Level.active_level.tick()
    
    for item in cannon_sys.Cannon_Ball.cannon_projectiles:
        if item.y < -10:
            cannon_sys.Cannon_Ball.cannon_projectiles.remove(item)
            del item

    for enemy in e.Enemy.enemy_list:
        pass

    #--------------------- Display Updates ---------------------#
    
    
    for sprite in c.Sprite.active_sprites:
        #pygame.draw.rect(screen, (255,0,0), sprite.rect)
        if sprite != player:
            sprite.tick()

    for i in cannons:
        screen.blit(i.image, i.rect)
            
    player.p_update(c.Platform.platform_list)
        

    
    pygame.display.flip()
    clock.tick(60) 


pygame.quit()