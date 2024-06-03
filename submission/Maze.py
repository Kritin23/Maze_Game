#Maze module
#implements maze class, maze generation and collision detection

from Utilities import *
from Player import *
import random
import numpy as np

class Maze:
	blockSize = 84
	wallSize = 10  
	
	'''
	initialize an instance of the maze class
	Arguments:
		size: size of maze

	Optional Arguments:
		cycles: number of cycles
		ghosts: no of ghosts
		traps: no. of traps
		trapEvent: event to handle for switching traps, necessary if traps>0
		lives: no. of lives
		timer: maze timer
		bullets: initial no. of bullets the player starts with
		blocks: no. of blocks in maze

	'''
	def __init__(self, size:int, **kwargs):
		self.score = 0
		cycles = kwargs["cycles"] if "cycles" in kwargs else 0
		self.allowedEdges, self.blockedEdges = GenerateMaze(size, cycles)
		self.size = size
		self.adjList = GetAdjList(self.allowedEdges, size**2)
		self.solution = FindPath(0,size**2-1,size**2,self.adjList)
		SavePath(self.solution, self.adjList, self.size)

		paths = []
		deadends = []

		for idx,node in enumerate(self.adjList):
			if(len(node) == 1):
				deadends.append(idx)
			else:
				paths.append(idx)

		if 0 in paths: paths.remove(0)
		if size**2-1 in paths: paths.remove(size**2-1)
		if 0 in deadends: deadends.remove(0)
		if size**2-1 in deadends: deadends.remove(size**2-1)


		self.trapCount=0
		if "traps" in kwargs:
			self.trapCount=kwargs["traps"]

		self.blockCount = 0
		if "blocks" in kwargs:
			self.blockCount = kwargs["blocks"]
		
		randomNo = np.random.choice(paths, (self.trapCount+self.blockCount))
		randomNoCounter=0
		self.blocksgridID = randomNo
			

		self.player = Player((self.blockSize/2, self.blockSize/2), "res/img/playerSprite.png", "res/img/fire.png")
		if "bullets" in kwargs:
			self.player.bullets = kwargs["bullets"]
		self.image, self.blockedRects = GenerateMazeImage(size, self.blockedEdges)
		self.bullets = []

		self.GhostSpriteObject = GhostSprite("res/img/enemy/enemy_n.png", "res/img/enemy/enemy_s.png", "res/img/enemy/enemy_w.png", "res/img/enemy/enemy_e.png", "res/img/enemy/enemy_d.png")

		self.ghosts = []
		if "ghosts" in kwargs:
			for i in range(kwargs['ghosts']):
				gx,gy = random.randint(1,size-1), random.randint(1,size-1)
				while (gy*size+gx in self.blocksgridID):
					gx,gy = random.randint(1,size-1), random.randint(1,size-1)
				##print(location)
				self.ghosts.append(Ghost((gx*Maze.blockSize + Maze.blockSize/2, gy*Maze.blockSize + Maze.blockSize/2), self.GhostSpriteObject))

		self.portals = []
		if "portals" in kwargs:
			if kwargs["portals"] > 0:
				noPortals = max(kwargs["portals"], 3)
				for i in range(noPortals):
					broadID1 = random.randint(0,8)
					broadID2 = random.randint(0,8)
					while broadID2 == broadID1:
						broadID2 = random.randint(0,8)
					narrowID1 = random.randint(0,(size//3)**2-1)
					narrowID2 = random.randint(0, (size//3)**2-1)
					def getId(broad, narrow):
						return (broad%3)*(size//3)+narrow%(size//3)+((broad//3)*(size//3)+narrow//(size//3))*size
					while(getId(broadID1, narrowID1) in self.blocksgridID):
						narrowID1 = random.randint(0,(size//3)**2)
					while(getId(broadID2,narrowID2) in self.blocksgridID):
						narrowID2 = random.randint(0,(size//3)**2)
					id1 = getId(broadID1, narrowID1)
					id2 = getId(broadID2, narrowID2)
					print(id1,id2)
					pos1 = ((id1%size)*self.blockSize + self.blockSize/2 , (id1//size)*self.blockSize + self.blockSize/2)
					pos2 = ((id2%size)*self.blockSize + self.blockSize/2 , (id2//size)*self.blockSize + self.blockSize/2)
					self.portals.append(Portal(pos1, pos2))

		self.traps = []
		if "traps" in kwargs:
			for i in range(kwargs["traps"]):
				tx,ty = randomNo[randomNoCounter]%size, randomNo[randomNoCounter]//size
				randomNoCounter+=1
				self.traps.append(Trap((tx*Maze.blockSize + Maze.blockSize/2,ty*Maze.blockSize + Maze.blockSize/2)))
			if(kwargs["traps"] > 0):
				self.SWITCHTRAPS = kwargs["trapEvent"]
		self.blocksgridID = []
		self.blocks = []
		if "blocks" in kwargs:
			if kwargs["blocks"] > 0:
				for i in range(kwargs["blocks"]):
					bx,by = randomNo[randomNoCounter]%size, randomNo[randomNoCounter]//size
					self.blocksgridID.append(randomNo[randomNoCounter])
					randomNoCounter+=1
					self.blocks.append(Block((bx*Maze.blockSize + Maze.blockSize/2, by*Maze.blockSize + Maze.blockSize/2),""))
					#print(bx,by)
		
		self.collectibles = []
		#10% of maze are collectibles
		#70%coins
		#20%bullets
		#10%lives
  
		collectibleSpriteObj = CollectibleSprite("res/img/coin.png", "res/img/heart.png", "res/img/potion.png")

		collectibleLoc = self.blocksgridID
		prob1 = np.ones((len(collectibleLoc)))
		prob1.fill(15)
		collectibleLoc.extend(deadends)
		prob2 = np.ones((len(deadends)))
		prob2.fill(2.5)
		collectibleLoc.extend(paths)
		prob3 = np.ones((len(paths)))
		prob3.fill(1)
		prob1 = np.concatenate((prob1,prob2,prob3), axis=-1)

		prob1 /= np.sum(prob1)

		choices = np.random.choice(collectibleLoc, ((size**2)//10), replace=False, p=prob1)

		for i in range(len(choices)):
			cX = self.blockSize*(choices[i]%size)+self.blockSize/2
			cY = self.blockSize*(choices[i]//size)+self.blockSize/2
			if(i<0.7*len(choices)):
				self.collectibles.append(Collectible((cX,cY), "coin", collectibleSpriteObj))
			elif(i<0.9*len(choices)):
				self.collectibles.append(Collectible((cX,cY), "bullet", collectibleSpriteObj))
			else:
				self.collectibles.append(Collectible((cX,cY), "life", collectibleSpriteObj))

		
		self.hitStatus = True #True means can hit
		self.HITRESTORE = pygame.USEREVENT+6




		if "lives" in kwargs:
			self.lives = kwargs["lives"]
			self.totalLives = self.lives
		else:
			self.lives = 3
			self.totalLives = 3
		
		if "timer" in kwargs:
			self.timer = kwargs["timer"]
		else:
			self.timer = 30

		#store locations of objects as indices of respective arrays
		#index 0: blockedRects(maze-walls)
		#index 1: player
		#index 2: bullets
		#index 3: ghosts	
        #index 4: traps
		#index 5: walls [destructible blocks]
		#index 6: collectibles
		self.objectLocations = [([],[],[],[],[],[],[]) for i in range(size**2)]
		self.UpdateObjectLocations(self.blockedRects, 0)
		self.UpdateObjectLocations([g.GetRect() for g in self.ghosts], 3)
		self.UpdateObjectLocations([t.GetRect() for t in self.traps], 4)
		self.UpdateObjectLocations([b.GetRect() for b in self.blocks], 5)
		self.UpdateObjectLocations([c.GetRect() for c in self.collectibles], 6)

		#portal variables
		self.TRANSPORT = pygame.USEREVENT + 7
		self.RESUME_COLLISIONS = pygame.USEREVENT + 8
		self.FIRE_ANIMATION = pygame.USEREVENT + 9
		self.transporting = False
		self.Colliding = True
		self.transportTarget = (-1,-1)

		#sounds
		self.PLAY_STEP_SOUND = pygame.USEREVENT + 10

		self.playerMoveSound = pygame.mixer.Sound("res/sound/step.wav")
		self.playerMoveSound.set_volume(0.5)
		self.teleportSound = pygame.mixer.Sound("res/sound/port.wav")
		self.attackSound = pygame.mixer.Sound("res/sound/attack.wav")
		self.wallHitSound = pygame.mixer.Sound("res/sound/wall_hit.wav")
		self.enemyDieSound = pygame.mixer.Sound("res/sound/enemy_die.wav")
		self.collectibleSound = pygame.mixer.Sound("res/sound/collect.wav")
		self.playerDieSound = pygame.mixer.Sound("res/sound/player_die.wav")

		pygame.time.set_timer(self.PLAY_STEP_SOUND, 500, 0)

	def EventHandler(self, event:pygame.event.Event):
		if(event.type == self.PLAY_STEP_SOUND and self.player.velocity.abs() > 1):
			pygame.mixer.Sound.play(self.playerMoveSound)
		
		if(event.type == pygame.KEYDOWN ):
			if(event.key == pygame.K_SPACE):
				if(self.player.bullets > 0):
					self.bullets.append(CreateBullet(self.player.GetCenter(), self.player.direction))
					self.player.bullets -= 1
			if(event.key == pygame.K_h and self.hitStatus):
				self.hitStatus = False
				pygame.time.set_timer(self.HITRESTORE, 400, 1)
				playerExRect = self.player.GetExtendedRect()
				for idx, b in enumerate(self.blocks):
					if(RectCollide(playerExRect, b.GetRect())):
						pygame.mixer.Sound.play(self.attackSound)
						x = b.Click()
						if(x == True):
							self.score+=75
							self.blocks.remove(b)
							self.UpdateObjectLocations([b.GetRect() for b in self.blocks], 5)
						break

			if(event.key == pygame.K_p):
				playerRect = self.player.GetRect()
				for p in self.portals:
					if(p.Collide(playerRect)):
						self.transporting = True
						self.Colliding = False
						self.player.transporting = True
						self.player.fireAnimationDir = 1
						pygame.time.set_timer(self.TRANSPORT, 400, 1)
						pygame.time.set_timer(self.RESUME_COLLISIONS, 1120, 1)
						pygame.time.set_timer(self.FIRE_ANIMATION, 70, 16)
						self.transportTarget = p.GetTransferPosition(playerRect)
						self.player.StopPlayer()
						pygame.mixer.Sound.play(self.teleportSound)
						break;
			
		if(event.type == self.TRANSPORT):
			self.player.SetPosition(self.transportTarget)
		if(event.type == self.RESUME_COLLISIONS):
			print("here")
			self.transportTarget = (-1,-1)
			if(not self.transporting): self.Colliding = True
			else:
				self.transporting = False
				pygame.time.set_timer(self.RESUME_COLLISIONS, 2000, 1)
		if(event.type == self.FIRE_ANIMATION):
			self.player.UpdateFireAnimation()

		
				
		if(event.type == self.HITRESTORE): 	self.hitStatus = True


		
		if(self.trapCount>0 and event.type == self.SWITCHTRAPS):
			for t in self.traps:
				if(not RectCollide(self.player.GetCollideRect(), t.GetRect())):
					t.SwitchState()
		#test
		if(event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_t]):
			#test code
			self.test()

	def MouseClick(self, mouseP):
		playerExRect = self.player.GetExtendedRect()
		for idx, b in enumerate(self.blocks):
			if(PointRectCollide(mouseP, b.GetRect()) and RectCollide(playerExRect, b.GetRect())):
				x = b.Click()
				if(x == True):
					self.score += 75
					self.blocks.remove(b)
					self.UpdateObjectLocations([b.GetRect() for b in self.blocks], 5)
				break

	def test(self):
		print(self.objectLocations)

	def Update(self, dT: float):
		#update velocities
		validKeyPress = False
		
		keys = pygame.key.get_pressed()
		if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
			self.player.RespondToKeyPress(DIR.LEFT, dT)
			validKeyPress = True
			####print("l",end=" ")
		if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
			self.player.RespondToKeyPress(DIR.DOWN, dT)
			validKeyPress = True
			####print("d",end=" ")
		if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
			self.player.RespondToKeyPress(DIR.RIGHT, dT)
			validKeyPress = True
			####print("r",end=" ")
		if(keys[pygame.K_w] or keys[pygame.K_UP]):
			self.player.RespondToKeyPress(DIR.UP, dT)
			validKeyPress = True
			####print("u",end=" ")
		if(not validKeyPress):
			#no key pressed
			#####print("here")
			self.player.RespondToKeyPress(DIR.NONE, dT)
		
		if(not self.transporting): self.player.UpdateVelocity(dT)

		#update bullet positions
		for b in self.bullets:
			destroy = True
			while(destroy and b in self.bullets):
				destroy = b.UpdatePosition(dT)
				if(destroy): self.bullets.remove(b)


		#update ghost positions
		if(not self.transporting):
			for g in self.ghosts:
				g.UpdateVelocity(self.blockSize, self.size, self.adjList)
				g.UpdatePosition(dT)
				##print(g.path)

		#update object locations
		self.UpdateObjectLocations([b.GetRect() for b in self.bullets], 2)
		self.UpdateObjectLocations([g.GetRect() for g in self.ghosts], 3)

		
		playerX,playerY = self.player.GetPosition()
		playerVx,playerVy = self.player.velocity.x, self.player.velocity.y
		playerH,playerW = self.player.h, self.player.w

		playerBroadRect = (playerX, playerY, playerVx*dT + playerW, playerVy*dT + playerH)
		self.playerBroadRect = playerBroadRect
		self.UpdateObjectLocations([playerBroadRect], 1)

		#check bullet-ghost, bullet-wall, ghost-wall collisions
		self.BulletCollision()

		#check player-wall collisions
		self.PlayerWallCollisions(dT)
		
		#update player position
		self.player.UpdatePosition(dT)

		self.UpdateObjectLocations([g.GetRect() for g in self.ghosts], 3)
		self.playerDead = self.PlayerObstacleCollision()
		if(not self.Colliding): self.playerDead=False
		if(self.playerDead):	
			pygame.time.set_timer(self.PLAY_STEP_SOUND, 0, 0)
			pygame.mixer.Sound.play(self.playerDieSound)
			self.score -= 100
			return False

		return True

	'''
	update the objectlocations data at index i with objectRects
	Arguments:
		objectRects: Rectangles of objects to update the data
		index: location where data is to be stored in objectLocations list
	'''
	def UpdateObjectLocations(self, objectRects: list, index: int):
		for gridSquare in self.objectLocations:
			gridSquare[index].clear()
		for i,rect in enumerate(objectRects):
			x,y,w,h = rect
			baseSquareID = int(y//Maze.blockSize * self.size + min(x // Maze.blockSize, self.size))
			topRightID = int(y//Maze.blockSize * self.size + min((x+w) // Maze.blockSize, self.size))
			bottomLeftID = int((y+h)//Maze.blockSize * self.size + min(x // Maze.blockSize, self.size))

			for k in range(baseSquareID,bottomLeftID+1,self.size):
				for j in range(topRightID-baseSquareID+1):
					if(k+j < self.size**2):
						self.objectLocations[k+j][index].append(i)

	'''
	Returns current win state
		0 if game is running
		-1 if game lost
		2 if player just died
		1 if game won
	'''
	def CheckWinState(self):
		playerCentre = self.player.GetCenter()
		targetLocation = (Maze.blockSize * (self.size - 0.625), Maze.blockSize * (self.size - 0.625), Maze.blockSize*0.5, Maze.blockSize*0.5)
		if(self.playerDead):
			if(self.lives == 0): return -1
			else: return 2
		elif(self.timer <= 0): return -1
		elif(playerCentre[0] >= targetLocation[0] and playerCentre[1] >= targetLocation[1] \
	   			and playerCentre[0] <= targetLocation[0]+targetLocation[2] \
					  and playerCentre[1] <= targetLocation[1]+targetLocation[3]):
			return 1
		else:
			return 0	

	'''
	All Bullet Collisions
	Also handles object destruction
	'''
	def BulletCollision(self):
		destroyBullet = [False for b in self.bullets]
		destroyGhost = [False for g in self.ghosts]
		destroyBlock = [False for b in self.blocks]
		for rect in self.objectLocations:
			for bullet in rect[2]:
				bulletRect = self.bullets[bullet].GetRect()
				for wall in rect[0]:
					if (RectCollide(bulletRect, self.blockedRects[wall])):
						destroyBullet[bullet] = True
				for ghost in rect[3]:
					ghostRect = self.ghosts[ghost].GetRect()
					if (not self.ghosts[ghost].dead and RectCollide(bulletRect, ghostRect)):
						pygame.mixer.Sound.play(self.enemyDieSound)
						destroyBullet[bullet] = True
						self.score += 100
						self.ghosts[ghost].SetDead()
					if(self.ghosts[ghost].dead and self.ghosts[ghost].currentAnimationFrame>=12):
						destroyGhost[ghost] = True

				for block in rect[5]:
					blockRect = self.blocks[block].GetRect()
					if(RectCollide(blockRect, bulletRect)):
						pygame.mixer.Sound.play(self.enemyDieSound)
						destroyBullet[bullet] = True
						x = self.blocks[block].Click()
						if x: destroyBlock[block] = True
				


		offset = 0
		for i in range(len(destroyBullet)):
			if(destroyBullet[i]):
				self.bullets.remove(self.bullets[i-offset])
				offset += 1
			i += 1

		offset = 0
		for i in range(len(destroyGhost)):
			if(destroyGhost[i]):
				self.ghosts.remove(self.ghosts[i-offset])
				offset += 1
			i += 1

		offset = 0
		for i in range(len(destroyBlock)):
			if(destroyBlock[i]):
				self.score += 75
				self.blocks.remove(self.blocks[i-offset])
				offset += 1
			i += 1

		if(np.any(np.asarray(destroyBlock)) == True):
			self.UpdateObjectLocations([b.GetRect() for b in self.blocks], 5)

	'''
	Handles player obstacle collisions and player dying
	'''
	def PlayerObstacleCollision(self):
		playerRect = self.player.GetCollideRect()
		collide = False
		cCollide = False
		destroyC = [False for c in range(len(self.collectibles))]
		for rect in self.objectLocations:
			if (len(rect[1])>0 and len(rect[3])>0):
				#print("here")
				for gID in rect[3]:
					if( (not self.ghosts[gID].dead) and  RectCollide(playerRect, self.ghosts[gID].GetCollideRect())):
						collide = True
						#print("die")
	  
			if(len(rect[1]) > 0 and len(rect[4])>0):
				for tID in rect[4]:
					if(self.traps[tID].currentState and RectCollide(playerRect,self.traps[tID].GetCollideRect())):
						collide = True
			if(len(rect[1]) > 0 and len(rect[6]) > 0):
				for cID in rect[6]:
					if(RectCollide(playerRect, self.collectibles[cID].GetRect())):
						match(self.collectibles[cID].type):
							case 1:
								self.score +=100
							case 2:
								self.lives += 1
							case 3:
								self.player.bullets += 10
						pygame.mixer.Sound.play(self.collectibleSound)
						destroyC[cID] = True
						cCollide = True
		offset = 0
		for i in range(len(destroyC)):
			if(destroyC[i]):
				self.collectibles.remove(self.collectibles[i-offset])
				#print("hit")
				offset += 1
			i += 1

		if cCollide:
			self.UpdateObjectLocations([c.GetRect() for c in self.collectibles], 6)
		return collide


	'''
	handles player wall collisions to stop player from moving
	'''
	def PlayerWallCollisions(self, dT: float):
		collisions = []
		collisions2 = []

		timeLeft = dT
		while(timeLeft > 0.0001):
			collideTime = 1
			collideNormal = Vec2(0,0)
			collided = False

			for gridRect in self.objectLocations:
				if(len(gridRect[1]) > 0):
					
					#walls
					for wallID in gridRect[0]:
						if(RectCollide(self.playerBroadRect, self.blockedRects[wallID])):
							collisions.append(wallID)

					#blocks
					for bID in gridRect[5]:
						if(RectCollide(self.playerBroadRect, self.blocks[bID].GetRect())):
							collisions2.append(bID)
	 	 			
			playerRect = self.player.GetRect()

			for box in collisions:
				time, normal = SweptAABB(playerRect, self.blockedRects[box], self.player.velocity, dT)
				##print("here", time, normal, self.player.velocity, self.player.position, self.blockedRects[box], dT)
				if(time < 1 and time < collideTime and time>=0):
					collideTime = time
					collideNormal = normal
					collided = True
				elif time < 0:
					collideNormal = normal
					collideTime = time
					collided = True
					break

			for box in collisions2:
				time, normal = SweptAABB(playerRect, self.blocks[box].GetRect(), self.player.velocity, dT)
				if(time < 1 and time < collideTime and time>=0):
					collideTime = time
					collideNormal = normal
					collided = True
				elif time < 0:
					collideNormal = normal
					collideTime = time
					collided = True
					break
			if not collided:
				break
			
			#response
			if collideTime <0:
				##print("inside collision")
				finalVelocity = self.player.velocity - collideNormal*(2*(self.player.velocity*collideNormal))
				self.player.velocity = finalVelocity
				self.player.UpdatePosition(dT)
				timeLeft += collideTime
				pygame.mixer.Sound.play(self.wallHitSound)
				break

			elif(collideTime < 1 and collideTime >= 0):
				##print("collision")
				self.player.UpdatePosition(collideTime)
				finalVelocity = self.player.velocity - collideNormal*(self.player.velocity*collideNormal)
				self.player.velocity = finalVelocity
				timeLeft -= collideTime
				pygame.mixer.Sound.play(self.wallHitSound)	



	'''
	Returns a b/w maze image
	redundant
	'''
	def GetImage(self):
		return self.image

	'''
	return score change since last time the function was called
	'''
	def GetScoreChange(self):
		x = self.score
		self.score = 0
		return x

	def CreatePlayer(self):
		self.player = Player((self.blockSize/2, self.blockSize/2), "res/img/playerSprite.png", "res/img/fire.png", bullets=self.player.bullets)
		noGhosts = len(self.ghosts)
		self.ghosts.clear()
		for i in range(noGhosts):
			gx,gy = random.randint(1,self.size-1), random.randint(1,self.size-1)
			while (gy*self.size+gx in self.blocksgridID):
				gx,gy = random.randint(1,self.size-1), random.randint(1,self.size-1)
			##print(location)
			self.ghosts.append(Ghost((gx*Maze.blockSize + Maze.blockSize/2, gy*Maze.blockSize + Maze.blockSize/2), self.GhostSpriteObject))
		self.transportTarget = (-1,-1)
		self.transporting=False
		self.Colliding=True
		pygame.time.set_timer(self.PLAY_STEP_SOUND, 500, 0)

'''
Better Maze Image Generatin available in Camera Module
DO NOT USE for Image Generation
USE Only for Blocked-Rects Generation

Generate a pygame surface of maze walls
Arguments
	n: size of maze
	blockedEdges: edges which are walls
Return
	instance of pygame surface with dimensions (n * blockSize X n * blockSize), list of blocked rectangles
'''
def GenerateMazeImage(n: int, blockedEdges: list[tuple[int,int]]):
	mazeImage = pygame.Surface((n*Maze.blockSize, n*Maze.blockSize))

	#Load Wall Sprite
	#plain rectangles for now
	horizontalWall = pygame.Surface((Maze.blockSize+Maze.wallSize, Maze.wallSize))
	verticalWall = pygame.Surface((Maze.wallSize, Maze.blockSize+Maze.wallSize))
	horizontalWall.fill((255,255,255))
	verticalWall.fill((255,255,255))

	#x y w h
	blockedRects = []

	#top wall
	blockedEdges.extend([(i-n, i) for i in range(n)])
	#bottom wall
	blockedEdges.extend([(n**2-1-i, n**2-i+n-1) for i in range(n)])

	for e  in blockedEdges:
		v1 = min(e[0], e[1])
		v2 = max(e[0], e[1])

		if(v2-v1 == 1):
			#horizontal edge, vertical wall
			wallX = round((v2 % n) * Maze.blockSize - Maze.wallSize//2)
			wallY = round((v2 // n) * Maze.blockSize -Maze.wallSize/2)
			mazeImage.blit(verticalWall, (wallX, wallY))
			blockedRects.append((wallX, wallY, Maze.wallSize, Maze.blockSize+Maze.wallSize))
		else:
			#vertical edge, horizontal wall
			wallX = round((v1 % n) * Maze.blockSize - Maze.wallSize/2)
			wallY = round((v2 // n) * Maze.blockSize - Maze.wallSize/2)
			mazeImage.blit(horizontalWall, (wallX, wallY))
			blockedRects.append((wallX, wallY, Maze.blockSize+Maze.wallSize, Maze.wallSize))
	
	#left and right walls
	for i in range(n):
		wallY = round(i * Maze.blockSize - Maze.wallSize/2)
		wallX1 = round(-Maze.wallSize/2)
		wallX2 = round(n * Maze.blockSize - Maze.wallSize/2)
		mazeImage.blit(verticalWall, (wallX1,wallY))
		mazeImage.blit(verticalWall, (wallX2, wallY))
		blockedRects.append((wallX1, wallY, Maze.wallSize, Maze.blockSize+Maze.wallSize))
		blockedRects.append((wallX2, wallY, Maze.wallSize, Maze.blockSize+Maze.wallSize))

	return mazeImage, blockedRects

'''
Generates a maze of size nxn and returns an instance of maze class
Starting square is top left, and target square is bottom right
'''
def GenerateMaze(n: int, cycles=0):
	edgeList = []
	for i in range(n):
		for j in range(n-1):
			#add node b/w i*n+j, i*n+j+1
			edgeList.append((i*n+j, i*n+j+1,random.random()))
	for i in range(n-1):
		for j in range(n):
			#add node b/w i*n+j, i*n+j+n
			edgeList.append((i*n+j, i*n+j+n,random.random()))
	edgeList = sorted(edgeList, key = lambda x:x[2])

	addedEdges = []
	removedEdges = []

	NodeSet = DisjointSet(n**2)

	counter = 0
	i = 0

	for e in edgeList:
		if(NodeSet.find(e[0]) != NodeSet.find(e[1])):
			addedEdges.append((e[0],e[1]))
			NodeSet.union(e[0],e[1])
			counter += 1
		else:
			removedEdges.append((e[0],e[1]))
		i+= 1
		if(counter >= n**2 - 1):    break

	#add some cycles in maze
	counter = 0
	while i < 2*(n**2 - n) and counter < cycles:
		addedEdges.append((edgeList[i][0],edgeList[i][1]))
		i+= 1
		counter += 1

	while i< 2*(n**2 - n):
		removedEdges.append((edgeList[i][0],edgeList[i][1]))
		i += 1
	return addedEdges, removedEdges

'''
Get Adjacency list of a graph
allowedEdges: list of tuple(u,v) where u,v are connected by an edge

return: a list of length n, where i-th list item contains all squares co[nnected to i via an edge]
'''
def GetAdjList(allowedEdges, n: int):
	adjList = [[] for j in range(n)]
	for e in allowedEdges:
		adjList[e[0]].append(e[1])
		adjList[e[1]].append(e[0])
	return adjList

'''
SweptAABB algorithm for continuous collision detection between a moving and a static axis-aligned boxes
Arguments:
	rect1:  moving box, (x,y,w,h)
	rect2:  static box, (x,y,w,h)
	v1: 	moving box velocity
Return:	tuple(dT, normal)
	time of collision between 0 and 1, as a percentage of dT
	if time < 0, collision already occured
	if time >= 1, collision did not occur
	normal: normal of static box surface that collided

reference: https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/swept-aabb-collision-detection-and-response-r3084/
'''
def SweptAABB(rect1, rect2, v1: Vec2, dT):
	x1,y1,w1,h1 = rect1
	x2,y2,w2,h2 = rect2
	#compute entry and exit distances along axes
	if(v1.x > 0):
		xEntryD = x2 - (x1 + w1)
		xExitD = (x2+w2) - x1
	else:
		xEntryD = (x2+w2) - x1
		xExitD = x2 - (x1+w1)
	if(v1.y > 0):
		yEntryD = y2 - (y1 + h1)
		yExitD = (y2+h2) - y1
	else:
		yEntryD = (y2+h2) - y1
		yExitD = y2 - (y1+h1)

	#entry and exit times
	xEntry = (xEntryD / v1.x) if v1.x!=0 else float('-inf')
	yEntry = (yEntryD / v1.y) if v1.y!=0 else float('-inf')
	xExit = (xExitD / v1.x) if v1.x!=0 else float('inf')
	yExit = (yExitD / v1.y) if v1.y!=0 else float('inf')

	entryTime = max(xEntry, yEntry) / dT
	exitTime = min(xExit, yExit) / dT

	#already inside
	if(entryTime < 0 and exitTime > 0):
		if(xEntry > yEntry):
			if(xEntryD > 0):
				normal = Vec2(1, 0)
			else:
				normal = Vec2(-1, 0)
		else:
			if(yEntryD > 0):
				normal = Vec2(0, 1)
			else:
				normal= Vec2(0, -1)
		return entryTime, normal

	#no collision
	if(entryTime < exitTime or entryTime<0 or xEntry>1 or yEntry>1):
		return 1, Vec2(0, 0)
	else:
		if(xEntry > yEntry):
			if(xEntryD > 0):
				normal = Vec2(1, 0)
			else:
				normal = Vec2(-1, 0)
		else:
			if(yEntryD > 0):
				normal = Vec2(0, 1)
			else:
				normal= Vec2(0, -1)
		
		return entryTime, normal
