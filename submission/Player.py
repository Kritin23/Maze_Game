#Player Module
#Implements the Player Class

from Utilities import *
import pygame
import random
import math
colorKey = (0,0,0)

class Player:
	h = 48	#48
	w = 48	#48
	MAX_VEL = 75        #maximum velocity in pixels per second
	TOTAL_FRAMES = 24				#total number of frames in animation
	

	#Arguments:
	#   startPos: starting center (x,y) of player
	#   playerSpriteSheetPath: Path of spriteshee of player
	#	optional
	#	bullets: no. of bullets player has
	def __init__(self, startPos, playerSpriteSheetPath, fireSpriteSheetPath, **kwargs):
		self.position = Vec2(startPos[0], startPos[1])
		self.position -= Vec2(self.h/2, self.w/2)
		self.velocity = Vec2(0,0)       #velocity in pixels per second
		self.acceleration = Vec2(0,0)   #acceleraton in pixels per second squared 
		self.direction = DIR.NONE
		self.currentAnimationFrame = 0       #stores the current frame to render the player
		self.spriteSheet = SpriteSheet(playerSpriteSheetPath)
		self.fireSprite = SpriteSheet(fireSpriteSheetPath)
		self.transporting = False
		self.fireAnimationDir = 0
		self.fireAnimationFrame=0
		self.bullets = 20
		if "bullets" in kwargs:
			self.bullets = kwargs["bullets"]

	#Arguments:
	#   keyDir: direction of key pressed
	#   dT: time elapsed since last frame
	#Updates player acceleration, velocity
	def RespondToKeyPress(self, keyDir, dT):
		if(keyDir != DIR.NONE):
			match(keyDir):
				case(DIR.UP):
					self.acceleration.y -= 1000
				case(DIR.DOWN):
					self.acceleration.y += 1000
				case(DIR.LEFT):
					self.acceleration.x -= 1000
				case(DIR.RIGHT):
					self.acceleration.x += 1000
			self.direction = keyDir
				
			self.acceleration = (normalize(self.acceleration) * 700) - (self.velocity * 3)

		else:
			self.acceleration = self.velocity * -10

		self.acceleration.x = round(self.acceleration.x, 0)
		self.acceleration.y = round(self.acceleration.y, 0)

		if(self.acceleration.abs() > 700):	self.acceleration = normalize(self.acceleration) * 700
	
	#Stop All Player Movement
	def StopPlayer(self):
		self.velocity = Vec2(0,0)
		self.acceleration = Vec2(0,0)

	def UpdateVelocity(self, dT):
		self.velocity += self.acceleration * dT
		if(self.velocity.abs() <= 0):	self.velocity = Vec2(0,0)
		if(self.velocity.abs() >= 100): 	self.velocity = normalize(self.velocity) * 100

		#self.acceleration = self.velocity * -7

		if(self.velocity.abs() <= 0):
			self.acceleration = Vec2(0,0)

		if(self.acceleration.abs() > 700):	self.acceleration = normalize(self.acceleration) * 700

		self.velocity.x = round(self.velocity.x, 3)
		self.velocity.y = round(self.velocity.y, 3)

		#update movement direction
		vx = self.velocity * Vec2(1,0)
		vy = self.velocity * Vec2(0,1)
		'''
		if(abs(vx) > abs(vy)):
			if(vx>0):	self.direction = DIR.RIGHT
			if(vx<0):	self.direction = DIR.LEFT
		elif(abs(vy) > abs(vx)):
			if(vy>0):	self.direction = DIR.DOWN
			if(vy<0): 	self.direction = DIR.UP
		'''

	#Update Player position based on set velocity and direction
	#argument dT: time elapsed since last frame in seconds
	def UpdatePosition(self, dT):
		self.position += self.velocity * dT
	
	#returns an image of player to render to the screen
	def GetImage(self):
		if(self.direction == DIR.NONE):
			surface = self.spriteSheet.getFrame(48,48,1)
		match(self.direction):
			case DIR.UP:
				surface = self.spriteSheet.getFrame(48,48,1)
			case DIR.DOWN:
				surface = self.spriteSheet.getFrame(48,48,0)
			case DIR.LEFT:
				surface = self.spriteSheet.getFrame(48,48,2) 
			case DIR.RIGHT:
				surface = self.spriteSheet.getFrame(48,48,3)
		
		if(self.transporting):
			fireSurface = self.fireSprite.getFrame(48,48,self.fireAnimationFrame)
			surface.blit(fireSurface, (0,0))
		return surface
	
	def UpdateFireAnimation(self):
		self.fireAnimationFrame += self.fireAnimationDir
		if(self.fireAnimationFrame == 8):
			self.fireAnimationFrame = 7
			self.fireAnimationDir = -1
		if(self.fireAnimationFrame == -1):
			self.fireAnimationDir = 0
			self.fireAnimationFrame = 0
			self.transporting = False

	def SetPosition(self, pos):
		self.position = Vec2(pos[0], pos[1])
	'''
	return player's top-left corner as tuple (x,y)
	'''
	def GetPosition(self):
		return (self.position.x, self.position.y)
	
	'''
	return player's centre as tuple (x,y)
	'''
	def GetCenter(self):
		return (self.position.x + self.w/2, self.position.y+self.h/2)

	def GetRect(self):
		return (self.position.x, self.position.y, self.w, self.h)

	def GetExtendedRect(self):
		playerRect = [self.position.x, self.position.y, self.w, self.h]
		match(self.direction):
			case DIR.UP:
				playerRect[1] -= self.h
				playerRect[3] *= 2
			case DIR.DOWN:
				playerRect[3] *= 2
			case DIR.LEFT:
				playerRect[0] -= self.w
				playerRect[2] *= 2
			case DIR.RIGHT:
				playerRect[2] *= 2
		return (playerRect[0], playerRect[1], playerRect[2], playerRect[3])

	def GetCollideRect(self):
		return (self.position.x+self.w/4, self.position.y+self.h/4, self.h/2, self.w/2)

'''
Create an instance if the bullet class
arguments: player's center as tuple (x,y) and direction as DirEnum
returns an instance of bullet class
'''
def CreateBullet(playerCenter, playerDirection):
	bulletX, bulletY = playerCenter
	playerDirection = playerDirection if playerDirection != DIR.NONE else DIR.UP
	
	match (playerDirection):
		case DIR.UP:
			bulletY -= Player.h/2 - Bullet.h/2
		case DIR.DOWN:
			bulletY += Player.h/2 - Bullet.h/2
		case DIR.LEFT:
			bulletX -= Player.w/2 - Bullet.w/2
		case DIR.RIGHT:
			bulletX += Player.w/2 - Bullet.w/2
	bulletX -= Bullet.w/2
	bulletY -= Bullet.h/2

	newBullet = Bullet((bulletX,bulletY), playerDirection)
	return newBullet

class Bullet:
	h=10
	w=10
	velocity = 300
	MAX_DISTANCE = 300

	def __init__(self, startPos, direction):
		self.x, self.y = startPos
		self.direction = direction
		self.currentDistance = 0

	def GetImage(self):
		img = pygame.surface.Surface((10,10))
		img.fill((255,255,255))
		return img
	
	def GetPosition(self):
		return (self.x, self.y)
	
	'''
	Returns bullet rectangle as tuple (x,y,w,h)
	'''
	def GetRect(self):
		return (self.x, self.y, self.w, self.h)

	#Updates position of the bullet on the screen
	#argument dT: time elapsed since last frame
	#return :
	#	True: if object is to be deleted, False otherwise
	def UpdatePosition(self, dT):
		match(self.direction):
			case DIR.UP:
				self.y -= self.velocity * dT
			case DIR.DOWN:
				self.y += self.velocity * dT
			case DIR.RIGHT:
				self.x += self.velocity * dT
			case DIR.LEFT:
				self.x -= self.velocity * dT
		if(self.direction != DIR.NONE):		self.currentDistance += self.velocity * dT
		if(self.currentDistance > self.MAX_DISTANCE):	return True
		else:	return False	

'''
class to extract images from ghost sprite sheets
'''
class GhostSprite():
	'''
	arguments: paths to corresponding spritesheets
	'''
	def __init__(self, pathN, pathS, pathW, pathE, pathDeath):
		self.spriteN = SpriteSheet(pathN)
		self.spriteE = SpriteSheet(pathE)
		self.spriteS = SpriteSheet(pathS)
		self.spriteW = SpriteSheet(pathW)
		self.spriteD = SpriteSheet(pathDeath)
	
	def GetImage(self, frame, direction, outputDim):
		match(direction):
			case (DIR.UP):
				return pygame.transform.scale(self.spriteN.getFrame(256, 256, frame), outputDim)
			case (DIR.DOWN):
				return pygame.transform.scale(self.spriteS.getFrame(256, 256, frame), outputDim)
			case (DIR.LEFT):
				return pygame.transform.scale(self.spriteW.getFrame(256, 256, frame), outputDim)
			case (DIR.RIGHT):
				return pygame.transform.scale(self.spriteE.getFrame(256, 256, frame), outputDim)
			case (DIR.NONE):
				return pygame.transform.scale(self.spriteN.getFrame(256, 256, frame), outputDim)
			case (-1):
				return pygame.transform.scale(self.spriteD.getFrame(256, 256, frame), outputDim)

class Ghost():
	h = 56
	w = 56
	MAX_VEL = 100
	TOTAL_FRAMES = 8

	#Arguments:
	#   startPos: starting center (x,y) of ghost
	#   ghostSpriteSheetPath: Path of spritesheet of ghost
	def __init__(self, startPos, ghostSpriteObj):
		self.position = Vec2(*startPos)
		self.position -= Vec2(self.h/2, self.w/2)
		self.velocity = Vec2(0,0)
		self.direction = DIR.NONE
		self.currentAnimationFrame = 0
		self.dead = False

		self.path = []
		self.spriteObj = ghostSpriteObj
    
	def SetPath(self,path):
		self.path = path

	def ResetPath(self):
		self.path = []

	def GetCollideRect(self):
		return (self.position.x+self.w/4, self.position.y+self.h/4, self.h/2, self.w/2)

	'''
	Updates velocity of ghost randomly
	allowedDirections: directions in which the ghost can currently move
	'''
	def UpdateVelocity(self, mazeBlockSize: int, mazeSize: int, mazeAdjList):
		xG,yG = self.GetCenter()
		currentSquare =int(xG // mazeBlockSize + (yG// mazeBlockSize)*int(mazeSize))
		currentSquare = min(currentSquare, mazeSize**2-1)
		ind = ListFind(self.path,currentSquare)
		if(len(self.path) > 1):
			if(ind == len(self.path)):
				self.SetPath(FindPath(currentSquare, self.path[-1], mazeSize**2, mazeAdjList))
				#print(self.path)
				nextSquare = self.path[1]
			elif(ind < len(self.path)-1):
				nextSquare = self.path[ind+1]
			else:
				x = currentSquare
				while(x == currentSquare):	x = random.randint(0,mazeSize**2-1)
				self.path = FindPath(currentSquare, x, mazeSize**2, mazeAdjList)
				#print(self.path)
				nextSquare=self.path[1]
		else:
			x = currentSquare
			while(x == currentSquare):	x = random.randint(0,mazeSize**2-1)
			self.SetPath(FindPath(currentSquare, x, mazeSize**2, mazeAdjList))
			nextSquare=self.path[1]

		currentSquarePosition = Vec2(
			int((0.5 + (currentSquare % mazeSize)) * mazeBlockSize),
			int((0.5 + (currentSquare // mazeSize)) * mazeBlockSize)
		)
		#print("currSqID: ", currentSquare, "nextSqID:", nextSquare)

		#print("sqCentre: ", currentSquarePosition, "g: ", self.GetCenter())

		nextSquarePosition = Vec2(
			int((0.5 + (nextSquare % mazeSize)) * mazeBlockSize),
			int((0.5 + (nextSquare // mazeSize)) * mazeBlockSize)
		)
		Cx,Cy = self.GetCenter()
		centre = Vec2(Cx,Cy)
		if(nextSquare == currentSquare+1):
			rect = (currentSquarePosition.x-5, currentSquarePosition.y-1,mazeBlockSize, 11)
		elif(nextSquare==currentSquare-1):
			rect = (nextSquarePosition.x+5, nextSquarePosition.y-5,mazeBlockSize, 11)
		elif(nextSquare==currentSquare+mazeSize):
			rect = (currentSquarePosition.x-5, currentSquarePosition.y-5,11, mazeBlockSize)
		else:
			rect = (nextSquarePosition.x-5, nextSquarePosition.y+5,11, mazeBlockSize)


		if (Cx>=rect[0] and Cy >= rect[1] and Cx<=rect[0]+rect[2] and Cy <= rect[1]+rect[3]):
			##print("here1")
			target = nextSquarePosition
		else:
			#print("here2")
			target = currentSquarePosition

		self.velocity = (target - centre) * 10
		if(self.velocity.abs() > self.MAX_VEL):	self.velocity = normalize(self.velocity) * self.MAX_VEL
		
		vx = self.velocity * Vec2(1,0)
		vy = self.velocity * Vec2(0,1)
		if(abs(vx) > abs(vy)):
			if(vx>0):	self.direction = DIR.RIGHT
			if(vx<0):	self.direction = DIR.LEFT
		elif(abs(vy) > abs(vx)):
			if(vy>0):	self.direction = DIR.DOWN
			if(vy<0): 	self.direction = DIR.UP
	
	#updates position of the ghost
    #arguments:
	#	dT: Time elapsed in previous frame
	def UpdatePosition(self, dT):
		self.position += self.velocity * dT

	#returns an pygame surface of the ghosts
	def GetImage(self):
		img = self.spriteObj.GetImage(int(self.currentAnimationFrame), self.direction if not self.dead else -1, (self.w,self.h))
		self.currentAnimationFrame +=1
		if not self.dead:
			self.currentAnimationFrame %= self.TOTAL_FRAMES
		else:
			self.currentAnimationFrame = max(self.currentAnimationFrame, 12)
		return img

	#sets ghost to dead
	#ghost still exists for animation
	def SetDead(self):
		self.dead=True
		self.currentAnimationFrame=4
	
	def GetPosition(self):
		return (self.position.x, self.position.y)
	
	def GetCenter(self):
		return (self.position.x+self.w/2, self.position.y+self.h/2)
	
	def GetRect(self):
		return (self.position.x, self.position.y, self.w, self.h)
	
class TrapSprite():
	def __init__(self, path):
		self.sprite = SpriteSheet(path)

	def GetImage(self, args):
		frame = args["frame"]
		return self.sprite.getFrame(Trap.h, Trap.w, frame)

class Trap():
	h=54
	w=54
	def __init__(self, startPos):
		self.position = Vec2(startPos[0], startPos[1])
		self.position -= Vec2(self.w/2, self.h/2)
		self.currentAnimationFrame=0
		self.currentState = True		#True is open

	def SwitchState(self):
		self.currentState = not self.currentState

	def GetImage(self):
		#open ie animationframe 3
		if(not self.currentState):
			if(self.currentAnimationFrame > 0):	self.currentAnimationFrame -= 1
			return {"frame": self.currentAnimationFrame}
		else:
			if(self.currentAnimationFrame < 3): self.currentAnimationFrame += 1
			return {"frame": self.currentAnimationFrame}
		
	def GetPosition(self):
		return (self.position.x, self.position.y)
	
	def GetRect(self):
		return (self.position.x, self.position.y, self.w, self.h)
	
	def GetCollideRect(self):
		return (self.position.x+self.w/8, self.position.y+self.h/8, 3*self.w/4, 3*self.h/4)

class BlockSprite():
	'''
	pathList: 3 paths - 1st state, 2nd state, 3rd state
	'''
	def __init__(self, pathList):
		self.state1 = pygame.image.load(pathList[0])
		self.state2 = pygame.image.load(pathList[1])
		self.state3 = pygame.image.load(pathList[2])
		self.state1 = pygame.transform.scale(self.state1, (Block.w, Block.h))
		self.state2 = pygame.transform.scale(self.state2, (Block.w, Block.h))
		self.state3 = pygame.transform.scale(self.state3, (Block.w, Block.h))

	'''
	Arguments:
	arg:
		frame: health of block
	'''
	def GetImage(self, arg):
		match(arg["frame"]):
			case 1:
				return self.state3
			case 2:
				return self.state2
			case 3:
				return self.state1

class Block():
	h=74
	w=74

	"""
	startPos: starting center position
	"""
	def __init__(self, startPos, spriteSheetPath):
		self.position = Vec2(startPos[0], startPos[1])
		print("initialized with position", self.position)
		self.position -= Vec2(self.w/2, self.h/2)
		self.health = 3
		#self.sprite = SpriteSheet(spriteSheetPath)
  
	def GetImage(self):
		return {"frame": self.health}
	
	def GetRect(self):
		return(self.position.x, self.position.y, self.w, self.h)
	
	def Click(self):
		self.health -= 1
		print("click")
		if(self.health <= 0):
			return True
		else:
			return False
		
	def GetPosition(self):
		return (self.position.x, self.position.y)
	
	def GetCenter(self):
		return (self.position.x + self.w/2, self.position.y + self.h/2)
	
class PortalSprite():
	def __init__(self, path):
		self.sprite = SpriteSheet(path)

	def GetImage(self, args):
		frame = args["frame"]
		return self.sprite.getFrame(Portal.h, Portal.w, frame)
class Portal():
	h=48
	w=48
	TOTAL_FRAMES=8

	'''
	pos1: position of first portal
	pos2: position of second portal
	'''
	def __init__(self, pos1, pos2):
		self.position1 = Vec2(pos1[0],pos1[1]) - Vec2(self.w/2, self.h/2)
		self.position2 = Vec2(pos2[0],pos2[1]) - Vec2(self.w/2, self.h/2)
		self.currentAnimationFrame = 0
		self.frameDir=1
	
	def GetRect1(self):
		return (self.position1.x, self.position1.y, self.w, self.h)
	def GetRect2(self):
		return (self.position2.x, self.position2.y, self.w, self.h)
	def GetPos1(self):
		return (self.position1.x, self.position1.y)
	def GetPos2(self):
		return (self.position2.x, self.position2.y)
	
	def GetTransferPosition(self, playerRect):
		if(RectCollide(playerRect, self.GetRect1())):
			return self.GetRect2()
		elif(RectCollide(playerRect, self.GetRect2())):
			return self.GetRect1()
		else:
			return playerRect
		
	def Collide(self, playerRect):
		if(RectCollide(playerRect, self.GetRect1()) or RectCollide(playerRect, self.GetRect2())):
			return True
		else:
			return False
		
	def GetImage(self):
		self.currentAnimationFrame += self.frameDir
		if(self.currentAnimationFrame >= self.TOTAL_FRAMES):
			self.frameDir *= -1
			self.currentAnimationFrame -= 2
		if(self.currentAnimationFrame <= 0):
			self.frameDir *= -1
			self.currentAnimationFrame += 2
		return {"frame": self.currentAnimationFrame}

class CollectibleSprite():
	def __init__(self, pathCoin, pathLife, pathBullet):
		self.spriteCoin = SpriteSheet(pathCoin)
		self.spriteLife = SpriteSheet(pathLife)
		self.spriteBullet = SpriteSheet(pathBullet)

	def GetImage(self, type):
		match(type):
			case 1:
				return self.spriteCoin.getFrame(30,30,0)
			case 2:
				return self.spriteLife.getFrame(30,30,0)
			case 3:
				return self.spriteBullet.getFrame(30,30,0)
		print("here")	
		return None



#common class for all collectible items
#Object oscillates vertically as y = Asin(t)
class Collectible():
	h=30
	w=30
	
	'''
	Arguments:
	startPos: starting position center
	type: string, such as life, bullet, coin
	'''
	def __init__(self, startPos, type, spriteObj):
		self.position = Vec2(startPos[0] - self.w/2, startPos[1] - self.h/2)
		self.phase = 0
		self.type = 0
		self.spriteObj = spriteObj
		match(type):
			case "coin":
				self.type = 1
			case "life":
				self.type=2
			case "bullet":
				self.type = 3
		

	def GetRect(self):
		return (self.position.x, self.position.y, self.w, self.h)
	
	def GetPosition(self):
		return (self.position.x,  self.position.y)

	def GetImage(self):
		return self.spriteObj.GetImage(self.type)
	
