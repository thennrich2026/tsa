
import gametimer as tm
from enemies import *
import settings as s


wavelist = {
	"basic": (("basic", "weak", 32, (100,100))),
	"valkery": (("diver", "weak", 5, (60,50)))
}


class Wave():
	def __init__(self,wavetype):
		self.wavetype = wavetype
		self.active = False
	
	def spawn_wave(self):
		wavetype = self.wavetype #OTHERWISE ITS UNHASHABLE RAHH
		
		if type(wavelist[wavetype][0]) == tuple:
			for enemies in wavelist[wavetype]: 
				initial_xy = x, y = enemies[3][0], enemies[3][1]
				for i in range(enemies[2]):
					enemy = init_enemy(enemies[0], enemies[1])
					x,y = enemy.spawn(x,y,initial_xy)
		else:
			enemies = wavelist[wavetype] 
			initial_xy = x,y = enemies[3][0],enemies[3][1]
			for i in range(enemies[2]):
				enemy = init_enemy(enemies[0],enemies[1])
				x,y = enemy.spawn(x,y,initial_xy)

class Level():
	active_level = None

	def __init__(self,wavelist,delay):
		self.delay = delay
		self.currentwave = None
		self.currentwavecount = 0
		self.wavelist = []
		self.active = False

		for wave in wavelist:
			self.wavelist.append(Wave(wave))

	def start(self):
		Level.active_level = self
		self.active = True
		if self.currentwave == None:
				self.currentwave = self.wavelist[self.currentwavecount]
				self.currentwave.spawn_wave()
		self.timer = tm.Timer(self.delay)

	def tick(self):
		if self.active:
			if self.timer.check():
				del(self.currentwave)
				self.currentwavecount+=1
				if self.currentwavecount >= len(self.wavelist):
					self.active = False
					Level.active_level = None
				else:
					self.currentwave = self.wavelist[self.currentwavecount]
					self.currentwave.spawn_wave()
					self.timer.restart()

	def end(self):
		del(self)
				



		
		
			
