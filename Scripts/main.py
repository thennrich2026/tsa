from regenerator import Regenerator
import sys, pygame, os, random, cannon_sys

pygame.init()

#imports
import enemies as e, classes as c, random, player_script
from settings import *
from levels import *
import gametimer

class Button():
    def __init__(self, image, image_scale):
        #creates the sprite's image and rect
        
        self.image_scale = image_scale
        self.image = pygame.transform.scale(image, (self.image_scale))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def update(self, mouse_pressed, mouse_pos, screen=settings.screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

        if mouse_pressed == True:
            if self.rect.colliderect(pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)) ==True:
                return True
        else:
            return False

class State_manager():
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

    def set_state(self, new_state):
        self.current_state = new_state
        self.setup_scene()
    
    #
    def setup_scene(self):
        states[self.current_state].setup()


class Menu():
    def __init__(self, display, state_manager):
        self.display = display
        self.game_state_manager = state_manager

    def run(self):
        screen.blit(self.bg, self.bg_rect)
        screen.blit(self.title, self.title_rect)
        
        mouse_1_state = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.update(mouse_1_state, mouse_pos) == True:
            self.game_state_manager.set_state('main')

    def setup(self):
        self.bg = img_dict["space_bg"]
        self.bg = pygame.transform.scale(self.bg, (900,900)) 
        self.bg_rect = self.bg.get_rect(center=(450,450)) 

        self.title = img_dict["title"]
        self.title_rect = self.title.get_rect(center=(450, 450))

        self.play_button = Button(img_dict['button'], (276, 125))
        self.play_button.x, self.play_button.y = (450, 550)


class Main():
    def __init__(self, display, state_manager):
        self.display = display
        self.game_state_manager = state_manager

    def setup(self):
        #screen setup
        c.Sprite.active_sprites = []
        c.Platform.platform_list = []
        e.Enemy.enemy_list = []
        cannon_sys.Cannon_Ball.cannon_projectiles = []

        self.bg = img_dict["space_bg"]
        self.bg = pygame.transform.scale(self.bg, (900,900)) 
        self.bg_rect = self.bg.get_rect(center=(450,450)) 

        #-- Center Platform and Cannon --#
        self.c_cannon = cannon_sys.Cannon(cannon_sys.cannon_dict['multishot']['multishot_1'])
        self.center_platform = c.Platform(img_dict["center_platform"], (310,40), self.c_cannon, (295, 750))
        self.center_platform.set_cannon_pos()
        self.c_base = c.Sprite(img_dict['cannon_base'], (57*2, 10*2))
        self.c_base.x = self.center_platform.rect.midtop[0] - 57
        self.c_base.y = self.center_platform.rect.midtop[1] - self.c_base.image_scale[1]

        #-- Left Platform and Cannon --#
        l_cannon = cannon_sys.Cannon(cannon_sys.cannon_dict['multishot']['multishot_1'])
        left_platform = c.Platform(img_dict["small_platform"], (210,40), l_cannon, (50,800))
        left_platform.set_cannon_pos()
        l_base = c.Sprite(img_dict['cannon_base'], (57*2, 10*2))
        l_base.x = left_platform.rect.midtop[0] - 58
        l_base.y = left_platform.rect.midtop[1] - self.c_base.image_scale[1]

        #-- Right Platform and Cannon --#
        r_cannon = cannon_sys.Cannon(cannon_sys.cannon_dict['multishot']['multishot_1'])
        self.right_platform = c.Platform(img_dict["small_platform"], (210,40), r_cannon, (650,800))
        self.right_platform.set_cannon_pos()
        self.r_base = c.Sprite(img_dict['cannon_base'], (57*2, 10*2))
        self.r_base.x = self.right_platform.rect.midtop[0] - 58
        self.r_base.y = self.right_platform.rect.midtop[1] - self.c_base.image_scale[1]
        

        self.cannons = [self.center_platform.cannon, self.c_base,  left_platform.cannon, l_base, self.right_platform.cannon, self.r_base]

        # Player setup
        self.player = player_script.Player_class(img_dict["player_stand"], (27*2, 50*2), 50)
        self.player.x = 450 -27
        self.player.y = 650

        #pre instanced code
        self.level1 = Level( ["basic"], 1000)
        self.level1.start()
        self.player_hp_bar = Health_Bar("Green", "Red", (60,10), self.player, 0, -25)

        # regenerator setup
        self.regenerator = Regenerator(img_dict["regenerator_1"], (67*2,34*2),25,5000)
        self.regenerator.x, self.regenerator.y = 450-67, 850-50
        self.regen_plat = Sprite(img_dict["small_platform"], (200,15))
        self.regen_plat.x, self.regen_plat.y = 450-200/2, 850+18

    def run(self):
        screen.blit(self.bg, self.bg_rect)
        
        #--------------------- Logic ---------------------#
        
        #Player logic
        keys = pygame.key.get_pressed()
        self.player.player_input(keys)
        
        if Level.active_level != None:
            Level.active_level.tick()
        
        for item in cannon_sys.Cannon_Ball.cannon_projectiles:
            if item.y < -10:
                cannon_sys.Cannon_Ball.cannon_projectiles.remove(item)
                c.Sprite.active_sprites.remove(item)
                del item

        for enemy in e.Enemy.enemy_list:
            for ball in cannon_sys.Cannon_Ball.cannon_projectiles:
                if enemy.rect.colliderect(ball.rect) == True:
                    enemy.onhit(ball)
                    cannon_sys.Cannon_Ball.cannon_projectiles.remove(ball)
                    c.Sprite.active_sprites.remove(ball)
                    del ball

        #--------------------- Display Updates ---------------------#
        
        
        for sprite in c.Sprite.active_sprites:
            #pygame.draw.rect(screen, (255,0,0), sprite.rect)
            if sprite != self.player:
                sprite.tick()

        for i in self.cannons:
            screen.blit(i.image, i.rect)
                
        self.player.p_update(c.Platform.platform_list)

clock = pygame.time.Clock()

state_manager = State_manager('menu')
menu = Menu(screen, state_manager)
main = Main(screen, state_manager)

states = {
    'menu' : menu,
    'main' : main
}

state_manager.setup_scene()


lit = ['main', 'menu']
index = 0
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Game Loop
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    states[state_manager.get_state()].run()

    pygame.display.flip()
    clock.tick(60) 


pygame.quit()