#Camera Module
#implements the camera class

import pygame
from Utilities import *

class Camera():
	H=400
	W=400
	PlayerSq=100
	MAX_VEL=150

	"""
	Arguments:
		camaeraOutput: required dimension of surface camera should output
		playerBox: The sideLength of the square in which player should be confined
		cameraCenter: The center of the player square relative to camera output surface
		minPos: minimum x,y the top-left of camera can have
		maxPos: maximum x,y the bottom-right of camera can have
	"""
	def __init__(self, cameraOutput, playerBox, cameraCenter, minPos, maxPos):
		assert cameraOutput[0] < maxPos[0] - minPos[0]
		assert cameraOutput[1] < maxPos[1] - minPos[1]
		assert cameraCenter[0] < cameraOutput[0]
		assert cameraCenter[1] < cameraOutput[1] 

		self.outputDim = cameraOutput
		self.playerBoxDim = playerBox
		self.center = Vec2(cameraCenter[0], cameraCenter[1])
		self.position = Vec2(minPos[0], minPos[1])	#camera x,y wrt maze (0,0)
		self.velocity = Vec2(0,0)
		self.minPos = minPos
		self.maxPos = maxPos
		self.night=False


	'''
	arguments:
		respective paths to sprite sheets
	'''
	def LoadMedia(self, wallLongPath, wallShortPath, tileOutPath, tileInPath):
		self.wallHorizontal = pygame.image.load(wallLongPath).convert_alpha()
		self.wallVertical = pygame.transform.rotate(self.wallHorizontal, 90).convert_alpha()
		self.wallShort = pygame.image.load(wallShortPath).convert_alpha()
		self.tileOut = pygame.image.load(tileOutPath).convert_alpha()
		self.tileIn = pygame.image.load(tileInPath).convert_alpha()

	'''
	arguments:
		wallLength: blockSize-wallWidth
		wallwidth: maze wall size
		blockSize: maze block size
		maze size: maze.size(count)
		blockedRects: list of walls
		kwargs:
			night: True
	'''
	def CreateMazeImage(self, wallLength, wallWidth, blockSize, mazeSize, blockedRects, **kwargs):
		self.ShadowLayer = pygame.Surface((mazeSize*blockSize, mazeSize*blockSize), pygame.SRCALPHA)
		self.WallLayer = pygame.Surface((mazeSize*blockSize, mazeSize*blockSize), pygame.SRCALPHA)
		self.BaseLayer = pygame.Surface((mazeSize*blockSize, mazeSize*blockSize))
		self.BackLayer = pygame.Surface(self.outputDim, pygame.SRCALPHA)
		self.CoverLayer = pygame.Surface((mazeSize*blockSize, mazeSize*blockSize), pygame.SRCALPHA)
		self.BackLayer.set_alpha(0)
		tileOutW = self.tileOut.get_width()
		tileOutH = self.tileOut.get_height()
		for i in range(self.outputDim[0] // tileOutW + 1):
			for j in range((self.outputDim[1] // tileOutH) + 1):
				self.BackLayer.blit(self.tileOut, (i*tileOutW, j*tileOutH))
		self.night = kwargs["night"] if "night" in kwargs else False
		mazeDim = mazeSize*blockSize

		#tile base layer
		for i in range(0, mazeDim//self.tileIn.get_width()+1):
			for j in range(0, mazeDim//self.tileIn.get_height()+1):
				self.BaseLayer.blit(self.tileIn, (i*self.tileIn.get_width(),j*self.tileIn.get_height()))
		
		self.CoverLayer.fill((0,0,0,160))
		if(self.night):
			self.BaseLayer.blit(self.CoverLayer, (0,0))
		self.light = pygame.image.load("res/img/light.png").convert_alpha()
		self.CoverLayer.fill((0,0,0,0))

		horWall = pygame.Surface((wallLength+0.5*wallWidth,wallWidth*1.5))
		horWall.fill((100,100,100))
		verWall = pygame.Surface((wallWidth*1.5,wallLength+0.5*wallWidth) )
		verWall.fill((100,100,100))
		for rect in blockedRects:
			if(rect[2] == wallWidth):
				self.ShadowLayer.blit(verWall, (rect[0],rect[1]))
			else:
				self.ShadowLayer.blit(horWall, (rect[0],rect[1]))
		self.ShadowLayer.set_alpha(100)

		corners = [ [ False for i in range(mazeSize+1) ] for j in range(mazeSize+1) ]

		horWall = pygame.Surface((wallLength,wallWidth))
		horWall.fill((0,0,255))
		verWall = pygame.Surface((wallWidth,wallLength) )
		verWall.fill((0,0,255))

		for rect in blockedRects:
			x,y,w,h=rect

			cornerI = (x+wallWidth//2)//blockSize
			cornerJ = (y+wallWidth//2)//blockSize
			corners[cornerI][cornerJ] = True
			#horizontal wall
			if(h==wallWidth):
				corners[cornerI+1][cornerJ]=True
				self.WallLayer.blit(self.wallHorizontal, (x+wallWidth,y))
			#vertical wall
			else:
				corners[cornerI][cornerJ+1]=True
				self.WallLayer.blit(self.wallVertical, (x,y+wallWidth))

		DarkSurface = pygame.Surface((blockSize,blockSize), pygame.SRCALPHA)
		DarkSurface.fill((0,0,0,190))

		for i in range(mazeSize+1):
			for j in range(mazeSize+1):
				x,y = i*blockSize, j*blockSize
				if(corners[i][j]):
					self.WallLayer.blit(self.wallShort, (x-wallWidth/2,y-wallWidth/2))
					if(self.night):
						self.CoverLayer.blit(self.light, (x-blockSize/2,y-blockSize/2))
				else:
					if(self.night):
						self.CoverLayer.blit(DarkSurface, (x-blockSize/2,y-blockSize/2))
		self.CoverLayer.set_alpha(200)

						

	"""
	Arguments:
		playerPosition: player center tuple in maze coordinates
		dT: Time elapsed in previous Frame
	"""
	def UpdatePosition(self, playerPosition, dT):
		playerRectLoc = self.position + self.center - Vec2(self.playerBoxDim/2, self.playerBoxDim/2)
		playerRect = (playerRectLoc.x, playerRectLoc.y, self.playerBoxDim, self.playerBoxDim)

		playerPos = Vec2(playerPosition[0],playerPosition[1])
		
		#position of camera center
		cameraPos = self.position + self.center

		maxVel = max(self.MAX_VEL, (playerPos - cameraPos).abs() * 3.5)

		#self.velocity = self.velocity * 0.1
		self.velocity = normalize(playerPos - cameraPos) * SmoothingFunction((playerPos - cameraPos).abs(), 0, maxVel, 3*self.playerBoxDim/8, self.playerBoxDim/8)
		#if(self.velocity.abs() < self.MAX_VEL/10):		self.velocity=Vec2(0,0)
		#self.velocity = vround(self.velocity)
		#print("error: ",vround((playerPos-cameraPos)), " velocity: ",vround(self.velocity))

		'''
		if(playerPosition[0] > playerRect[0] and playerPosition[1] > playerRect[1] \
	 		and playerPosition[0] < playerRect[0] + playerRect[2] and \
				playerPosition[1] < playerRect[1] + playerRect[3]):
			self.velocity = Vec2(0,0)'''

		self.position += self.velocity*dT
		if((self.velocity * dT).abs() < 1.5):
			self.position -= self.velocity*dT
			self.velocity = 0

		if(self.position.x < self.minPos[0]):	self.position.x=self.minPos[0]
		if(self.position.x + self.outputDim[0] > self.maxPos[0]):	self.position.x = self.maxPos[0] - self.outputDim[0]
		if(self.position.y < self.minPos[1]):	self.position.y=self.minPos[1]
		if(self.position.y + self.outputDim[1] > self.maxPos[1]):	self.position.y = self.maxPos[1] - self.outputDim[1]

	def ResetPosition(self):
		self.position = Vec2(self.minPos[0], self.minPos[1])

	'''
	Arguments:
		objects: List of tuples of the form (positionTuple, dimensionTuple, surfaceImage)
	
	Returns:
		pygame surface of dimension cameraOutput
	'''
	def GetImage(self, objects):
		cameraRect = (self.position.x, self.position.y, self.outputDim[0], self.outputDim[1])

		surface = pygame.Surface((self.outputDim[0], self.outputDim[1]), pygame.SRCALPHA)
		
		surface.blit(self.BackLayer, (0,0))
		mazeOrigin = ((-self.position.x), (-self.position.y))

		surface.blit(self.BaseLayer, mazeOrigin)
		for obj in objects:
			pos, dim, img = obj
			rect = (round(pos[0]), round(pos[1]), dim[0], dim[1])
			if(RectCollide(rect, cameraRect)):
				surface.blit(img, (mazeOrigin[0]+pos[0], mazeOrigin[1]+pos[1]))
		
		surface.blit(self.ShadowLayer, mazeOrigin)
		surface.blit(self.WallLayer, mazeOrigin)
		if(self.night):
			surface.blit(self.CoverLayer, mazeOrigin)
		return surface

	def GetRect(self):
		cameraRect = (self.position.x, self.position.y, self.outputDim[0], self.outputDim[1])
		return cameraRect
	
	def GetPosition(self):
		return (self.position.x, self.position.y)