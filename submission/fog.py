#a module to generate fog
import pygame
import random
import numpy as np


###
#Renders a fog effect
#generates particles of random size, location and alpha and renders them
#Dynamic fog: some particles grow in size and decrease in alpha
#Dynamic fog takes too long to render
class Fog:
	def __init__(self, outputDim, regionList):
		self.outputDim = outputDim
		self.regionsX = [(x[0],x[0]+x[2]) for x in regionList]
		self.regionsY = [(x[1], x[1]+x[3]) for x in regionList]
		self.counts = [x[4] for x in regionList]
		self.surface = pygame.Surface(self.outputDim, pygame.SRCALPHA)
		self.displaySurface = pygame.Surface(self.outputDim, pygame.SRCALPHA)
		self.particle = pygame.image.load("res/img/cloud.png").convert_alpha()
		self.particle.set_alpha(127)
		self.moving = []





		for i in range(len(regionList)):
			X = np.random.randint(self.regionsX[i][0], self.regionsX[i][1], size=(self.counts[i]))
			Y = np.random.randint(self.regionsY[i][0], self.regionsY[i][1], size=(self.counts[i]))
			S = np.random.randint(20,100,size=(self.counts[i]))
			A = np.random.randint(128,255,size=self.counts[i]) * (1 - S/150) * ((S/150)**2)
			for j in range(self.counts[i]):
				this_particle = pygame.transform.scale(self.particle, (S[j],S[j]))
				this_particle.set_alpha(A[j])
				self.surface.blit(this_particle, (X[j],Y[j]))
			
			#dynamic fog
			for j in range(int(0.025 * self.counts[i])):
				x = random.randint(self.regionsX[i][0], self.regionsX[i][1])
				y = random.randint(self.regionsY[i][0], self.regionsY[i][1])
				size = random.randint(20,100)
				a = random.randint(128,255)
				alpha = a * (1 - (size/150)) * (size/150)
				self.moving.append((x,y,size,a,i))
		self.displaySurface.blit(self.surface, (0,0))

	def Update(self, dT):
		self.displaySurface.fill((0,0,0,0))
		self.displaySurface.blit(self.surface,(0,0))
		for idx, p in enumerate(self.moving):
			x,y,size,a,r = p
			size += 70*dT
			if(size > 150):
				x = random.randint(self.regionsX[r][0], self.regionsX[r][1])
				y = random.randint(self.regionsY[r][0], self.regionsY[r][1])
				size = random.randint(20,100)
				alpha = random.randint(128,255) * (1 - (size/400)) * ((size / 150)**2)
			alpha = a * (1 - (size/150))
			this_particle = pygame.transform.scale(self.particle, (size,size))
			this_particle.set_alpha(alpha)
			self.displaySurface.blit(this_particle, (x-size/2,y-size/2))
			self.moving[idx] = (x,y,size,a,r)

	def GetImage(self):
		return self.displaySurface


'''
Arguments:
	outputDim: tuple(w,h)
	regionList: List(x,y,w,h,count) in which fog is to be placed
'''
def init(outputDim, regionList):
	global FogObject
	FogObject=Fog(outputDim, regionList)

def Update(dT):
	pass
	#FogObject.Update(dT)

def GetImage():
	return FogObject.GetImage()

def Quit():
	global FogObject
	del FogObject



"""
##Code used for testing the idea

DisplaySurface = pygame.display.set_mode(outputDim, 0, 32)

running = True

particle = pygame.image.load("res/img/cloud.png").convert_alpha()
particle.set_alpha(127)
count=1

imgs = []
surface = pygame.Surface(outputDim, pygame.SRCALPHA)

for i in range(3000):
	x = random.randint(-20,960)
	y = random.randint(-20,50)
	size = random.randint(20,100)
	alpha = random.randint(128,255) * (1 - (size/150)) * (size/150)
	this_particle = pygame.transform.scale(particle, (size,size))
	this_particle.set_alpha(alpha)
	surface.blit(this_particle, (x,y))

moving = [(random.randint(-20,960),random.randint(0,100), random.randint(20,100), random.randint(128,255))  for i in range(50)]

clock = pygame.time.Clock()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	DisplaySurface.fill((20,200,80))
	DisplaySurface.blit(surface, (0,0))
	for idx,i in enumerate(moving):
		x,y,size,a = i
		size += 0.07 * clock.get_time()
		if(size > 150):
			x = random.randint(-20,960)
			y = random.randint(0,100)
			size = random.randint(20,100)
			alpha = random.randint(128,255) * (1 - (size/400)) * (size / 150)
		alpha = a * (1 - (size/150))
		this_particle = pygame.transform.scale(particle, (size,size))
		this_particle.set_alpha(alpha)
		DisplaySurface.blit(this_particle, (x-size/2,y-size/2))
		moving[idx] = (x,y,size,a)

"""
