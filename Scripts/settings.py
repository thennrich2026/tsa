"""
This file is for global variables like the image_dict
"""
import pygame

running = True

size = width, height = 900, 900

screen = pygame.display.set_mode(size)
pausemomentum = False
enemy_bounce_x = 10

img_dict = {
    "space_bg": pygame.image.load("assets/space_bg_480x480.png").convert_alpha(),
    "center_platform" : pygame.image.load("assets/platforms/center_platform_155x15.png").convert_alpha(),
    "small_platform" : pygame.image.load("assets/platforms/small_platform_105x15.png").convert_alpha(),
    "basic" : pygame.image.load("assets/enemies/basic_40x40.png").convert_alpha(),
    "diver" : pygame.image.load("assets/enemies/diver_32x32.png").convert_alpha(),
    "player_jump" : pygame.image.load("assets/player/jump_27x50.png").convert_alpha(),
    "player_left" : pygame.image.load("assets/player/leftwalk_27x50.png").convert_alpha(),
    "player_right" : pygame.image.load("assets/player/rightwalk_27x50.png").convert_alpha(),
    "player_stand" : pygame.image.load("assets/player/stand_27x50.png").convert_alpha(),
    "bullet" : pygame.image.load("assets/bullet.png").convert_alpha(),
    "multishot_1" : pygame.image.load("assets/cannons/multishot_1_21x58.png").convert_alpha(),
    "multishot_2" : pygame.image.load("assets/cannons/multishot_2_25x58.png").convert_alpha(),
    "multishot_3" : pygame.image.load("assets/cannons/multishot_3_25x63.png").convert_alpha(),
    "error": pygame.image.load("assets/errorimage.png").convert_alpha(),
    "cannon_base" : pygame.image.load("assets/cannons/cannon_base_57x10.png").convert_alpha(),
    "sniper_1" : pygame.image.load("assets/cannons/sniper_1_21x66.png").convert_alpha(),
    "sniper_2" : pygame.image.load("assets/cannons/multishot_3_25x63.png").convert_alpha(),
    "sniper_3" : pygame.image.load("assets/cannons/multishot_3_25x63.png").convert_alpha(),
    "regenerator_1" : pygame.image.load("assets/regenerator_1_67x34.png").convert_alpha(),
    "title" : pygame.image.load("assets/title_900x900.png").convert_alpha(),
    "button" : pygame.image.load("assets/button_276x125.png").convert_alpha(),
}