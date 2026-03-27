import settings
import player_script as ps
import classes as c
import gametimer as t

class Regenerator(c.Sprite):
    active_regenerator = None
    def __init__(self, image, image_scale,hp,delay):
        c.Sprite.__init__(self,image,image_scale)
        self.hp = hp
        self.delay = delay
        self.timer = t.Timer(self.delay)
        self.regen = False
        Regenerator.active_regenerator = self

    def regenerate(self):
        #regen player
        self.timer.restart()
        self.regen = True
    
    def tick(self):
        self.update()
        if self.regen and self.timer.check():
            #regenerate
            pass
