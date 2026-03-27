import pygame


class Timer():
    def __init__(self,length:int):
        self.end = pygame.time.get_ticks()+length
        self.length = length
    def check(self): #returns true if timer has ended
        return pygame.time.get_ticks() >= self.end
    def restart(self):
        self.end = pygame.time.get_ticks()+self.length