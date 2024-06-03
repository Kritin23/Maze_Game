from Maze import *
import pygame
import os
from Camera import Camera
import Text
import fog

#GameState Module

#each game state is represented by an instance of a child class of the GameState class
#each child class implements init, enter, exit, eventHandler, render and update functions
#The Game Loop will call these functions and also switch between game states accordingly
#ChangeGameState function is for changing between game states 

#Base GameState Class
#All different GameStates will inherit from this class

SCREEN_HEIGHT = 640
SCREEN_WIDTH = 960

CLR_BROWN = pygame.Color(82,52,14)

CLR_KEY = pygame.Color(102,200,88)

class GameStateEnum:
	START_SCR=0
	PLAY_GAME=1
	GAMEOVER=2
	SAVE_SCORE=3
	LEADER_BRD=4
	NONE=5

GS = GameStateEnum()

'''
Class to implement game states

class members:
	current state stores current game state
	nextSTate stores the next state to be set to
	nextstateargs store the arguments to be passed to next state's enter in a dictionary
'''
class GameStateHandler:
	def __init__(self, currentState, stateArgs):
		self.allGameStates = [StartScreen(), PlayGame(), GameOver(), SaveScore(), LeaderBoard()] #a list of game state objects
		self.currentState = currentState
		self.nextState = GS.NONE
		self.nextStateArgs = {}

		if(currentState!= GS.NONE):		self.allGameStates[currentState].Enter(stateArgs)

	#Marks the next state to be set
	def SetNextState(self, nextState, stateArgs):
		self.nextState = nextState
		self.nextStateArgs = stateArgs

	#Set the next state
	def UpdateState(self):
		if(self.nextState != GS.NONE):
			if(self.currentState!=GS.NONE):		self.allGameStates[self.currentState].Exit()
			self.currentState = self.nextState
			self.allGameStates[self.currentState].Enter(self.nextStateArgs)
			self.nextState = GS.NONE
			self.nextStateArgs = {}

	#wrapper functions
	def EventHandler(self, event):
		if(self.currentState!= GS.NONE):	self.allGameStates[self.currentState].EventHandler(event, self)

	def Update(self, dT):
		if(self.currentState!= GS.NONE):	self.allGameStates[self.currentState].Update(dT, self)

	def Render(self, surface):
		if(self.currentState!= GS.NONE):	self.allGameStates[self.currentState].Render(surface)

	def Exit(self):
		if(self.currentState!= GS.NONE):	self.allGameStates[self.currentState].Exit()

#Base class for all game states
class GameState:
	def __init__(self):
		pass

	#event: pygame event
	#gsh: game state handler
	def EventHandler(self, event, gsh):
		pass

	#surface: screen surface
	def Render(self, surface):
		pass

	#dT: time elapsed
	#gsh: game state handler
	def Update(self, dT, gsh):
		pass

	#args: state args, a dictionary
	def Enter(self, args):
		pass

	def Exit(self):
		pass

class StartScreen(GameState):
	def __init__(self):
		pass
	
	#subState 1: Start Screen
	#subState 2: Level Select
	#substate 3: Instructions

	
	def Enter(self, args):
		self.subState = 1

		self.stateArgs = {"night": False}
		if "night" in args and args["night"]:
			self.stateArgs["night"]=True

		self.scrollH = pygame.image.load("res/img/scroll_h.png").convert_alpha()
		self.scrollH = pygame.transform.scale(self.scrollH, (450, 110))
		self.scrollV = pygame.image.load("res/img/scroll_v.png").convert_alpha()
		self.backG   = pygame.image.load("res/img/backg.png").convert_alpha()
		self.backGN  = pygame.image.load("res/img/backgN.png").convert_alpha()


		self.boldRender = -1

		self.playText = Text.render("Play", "Reg", 30, CLR_BROWN)
		self.instText = Text.render("Instructions", "Reg", 30, CLR_BROWN)
		self.leadText = Text.render("LeaderBoard", "Reg", 30, CLR_BROWN)
		self.playTextM = Text.render("Play", "M", 30, CLR_BROWN)
		self.instTextM = Text.render("Instructions", "M", 30, CLR_BROWN)
		self.leadTextM = Text.render("LeaderBoard", "M", 30, CLR_BROWN)

		self.chooseLevelText = Text.render("Choose a Level", "B", 60, CLR_BROWN)

		self.playRect = (SCREEN_WIDTH/2 - self.playText.get_width()/2-20, 340, self.playText.get_width()+40, self.playText.get_height())
		self.instRect = (SCREEN_WIDTH/2 - self.instText.get_width()/2-20, 390, self.instText.get_width()+40, self.instText.get_height())
		self.leadRect = (SCREEN_WIDTH/2 - self.leadText.get_width()/2-20, 440, self.leadText.get_width()+40, self.leadText.get_height())

		self.level1Text = Text.render("Level1", "Reg", 30, CLR_BROWN)
		self.level2Text = Text.render("Level2", "Reg", 30, CLR_BROWN)
		self.level3Text = Text.render("Level3", "Reg", 30, CLR_BROWN)
		self.level4Text = Text.render("Level4", "Reg", 30, CLR_BROWN)
		self.level5Text = Text.render("Bonus Level", "Reg", 30, CLR_BROWN)
		self.level1TextM = Text.render("Level1", "M", 30, CLR_BROWN)
		self.level2TextM = Text.render("Level2", "M", 30, CLR_BROWN)
		self.level3TextM = Text.render("Level3", "M", 30, CLR_BROWN)
		self.level4TextM = Text.render("Level4", "M", 30, CLR_BROWN)
		self.level5TextM = Text.render("Bonus Level", "M", 30, CLR_BROWN)

		self.level1Rect = (SCREEN_WIDTH/2 - self.level1Text.get_width()/2-20, 250, self.level1Text.get_width()+40, self.level1Text.get_height())
		self.level2Rect = (SCREEN_WIDTH/2 - self.level2Text.get_width()/2-20, 300, self.level2Text.get_width()+40, self.level2Text.get_height())
		self.level3Rect = (SCREEN_WIDTH/2 - self.level3Text.get_width()/2-20, 350, self.level3Text.get_width()+40, self.level3Text.get_height())
		self.level4Rect = (SCREEN_WIDTH/2 - self.level4Text.get_width()/2-20, 400, self.level4Text.get_width()+40, self.level4Text.get_height())
		self.level5Rect = (SCREEN_WIDTH/2 - self.level5Text.get_width()/2-20, 450, self.level5Text.get_width()+40, self.level5Text.get_height())


		backButton = pygame.image.load("res/img/small.png").convert_alpha()
		backText = Text.render("Main Menu", "Reg", 20, CLR_BROWN)
		backTextM = Text.render("Main Menu", "M", 20, CLR_BROWN)
		self.backButton = pygame.transform.scale(backButton, (155, 50))
		self.backButtonM = pygame.transform.scale(backButton, (155, 50))
		self.backButton.blit(backText, (20,10))
		self.backButtonM.blit(backTextM, (20,10))
		self.backButtonRect = (35, 35, 155, 50)

		#moon - bold render id 7
		self.moonImg = pygame.image.load("res/img/moon.png").convert_alpha()
		self.moonImg = pygame.transform.scale(self.moonImg, (55,55))
		self.Button = pygame.image.load("res/img/small.png").convert_alpha()
		self.Button = pygame.transform.scale(self.Button, (75,75))
		self.moonImgH = pygame.Surface((75,75), pygame.SRCALPHA)
		self.moonImgD = pygame.Surface((75,75), pygame.SRCALPHA)
		self.moonImgS = pygame.Surface((75,75), pygame.SRCALPHA)
		self.moonImgS.blit(self.Button, (0,0))
		self.moonImgD.blit(self.Button, (0,0))
		self.moonImgH.blit(self.Button, (0,0))
		self.moonImgH.blit(self.moonImg, (10,10))
		self.moonImg.set_alpha(220)
		self.moonImgS.blit(self.moonImg, (10,10))
		self.moonImg.set_alpha(110)
		self.moonImgD.blit(self.moonImg, (10,10))
		self.moonRect = (750, 550, 150, 150)

		#sound icon - bold render id 8
		self.speakerImg = pygame.image.load("res/img/speaker.png").convert_alpha()
		self.speakerImg = pygame.transform.scale(self.speakerImg, (55,55))
		self.Button = pygame.image.load("res/img/small.png").convert_alpha()
		self.Button = pygame.transform.scale(self.Button, (75,75))
		self.speakerImgH = pygame.Surface((75,75), pygame.SRCALPHA)
		self.speakerImgD = pygame.Surface((75,75), pygame.SRCALPHA)
		self.speakerImgS = pygame.Surface((75,75), pygame.SRCALPHA)
		self.speakerImgS.blit(self.Button, (0,0))
		self.speakerImgD.blit(self.Button, (0,0))
		self.speakerImgH.blit(self.Button, (0,0))
		self.speakerImgH.blit(self.speakerImg, (10,10))
		self.speakerImg.set_alpha(220)
		self.speakerImgS.blit(self.speakerImg, (10,10))
		self.speakerImg.set_alpha(110)
		self.speakerImgD.blit(self.speakerImg, (10,10))
		self.speakerRect = (150, 550, 150, 150)

		self.sound = True

		#instructions:
		self.scrollBig = pygame.image.load("res/img/scroll_v.png").convert_alpha()
		self.scrollBig = pygame.transform.scale(self.scrollBig, (750,400))
		self.line1 = Text.render("1. Reach the lost scroll to complete the level", "Reg", 25, CLR_BROWN)
		self.line2 = Text.render("2. Move using 'WASD' or arrow keys", "Reg", 25, CLR_BROWN)
		self.line3 = Text.render("3. Shoot spirits using 'SPACEBAR'", "Reg", 25, CLR_BROWN)
		self.line4 = Text.render("4. Destroy brick walls using 'H'", "Reg", 25, CLR_BROWN)
		self.line5 = Text.render("5. Teleport through portals using 'P'", "Reg", 25, CLR_BROWN)

		#sound
		self.menuSelectSound = pygame.mixer.Sound("res/sound/MenuSelect.mp3")

		#a mousemotion event at the start so that highlights can be set
		pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)

	def EventHandler(self, event, gsh: GameStateHandler):
		
		if(self.subState == 1):
			if(event.type == pygame.MOUSEMOTION):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.playRect)):
					self.boldRender = 1
				elif(PointRectCollide(mouseP, self.instRect)):
					self.boldRender = 2
				elif(PointRectCollide(mouseP, self.leadRect)):
					self.boldRender = 3
				elif(PointRectCollide(mouseP, self.moonRect)):
					self.boldRender = 7
				elif(PointRectCollide(mouseP, self.speakerRect)):
					self.boldRender = 8
				else:
					self.boldRender = -1
			if(event.type == pygame.MOUSEBUTTONDOWN):
				pygame.mixer.Sound.play(self.menuSelectSound)
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.playRect)):
					self.subState = 2
					self.boldRender = -1
					#a mousemotion event at the state change so that highlights can be set
					pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)
				elif(PointRectCollide(mouseP, self.instRect)):
					self.subState = 3
					self.boldRender = 2
					#a mousemotion event at the state change so that highlights can be set
					pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)
				elif(PointRectCollide(mouseP, self.leadRect)):
					gsh.SetNextState(GS.LEADER_BRD, {"night": self.stateArgs["night"]}) 
				elif(PointRectCollide(mouseP, self.moonRect)):
					self.stateArgs["night"] = (not self.stateArgs["night"])
				elif(PointRectCollide(mouseP, self.speakerRect)):
					self.sound = not self.sound
					if(self.sound):
						pygame.mixer.music.play(loops=-1)
					else:
						pygame.mixer.music.stop()
				else:
					self.boldRender = -1
		elif(self.subState == 2):
			if(event.type == pygame.MOUSEMOTION):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.level1Rect)):
					self.boldRender = 1
				elif(PointRectCollide(mouseP, self.level2Rect)):
					self.boldRender = 2
				elif(PointRectCollide(mouseP, self.level3Rect)):
					self.boldRender = 3
				elif(PointRectCollide(mouseP, self.level4Rect)):
					self.boldRender = 4
				elif(PointRectCollide(mouseP, self.level5Rect)):
					self.boldRender = 5
				elif(PointRectCollide(mouseP, self.backButtonRect)):
					self.boldRender = 0
				else:
					self.boldRender = -1
			elif(event.type == pygame.MOUSEBUTTONDOWN):
				pygame.mixer.Sound.play(self.menuSelectSound)
				stateArgs = {"level": 0, "night": self.stateArgs["night"]}
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.level1Rect)):
					stateArgs["level"] = 1
				elif(PointRectCollide(mouseP, self.level2Rect)):
					stateArgs["level"] = 2
				elif(PointRectCollide(mouseP, self.level3Rect)):
					stateArgs["level"] = 3
				elif(PointRectCollide(mouseP, self.level4Rect)):
					stateArgs["level"] = 4
				elif(PointRectCollide(mouseP, self.level5Rect)):
					stateArgs["level"] = 5
				elif(PointRectCollide(mouseP, self.backButtonRect)):
					self.subState = 1
					pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)
				else:
					self.boldRender = -1
				
				if(stateArgs["level"] != 0):
					gsh.SetNextState(GS.PLAY_GAME, stateArgs)
		elif(self.subState == 3):
			mouseP = pygame.mouse.get_pos()
			if(event.type == pygame.MOUSEMOTION):
				if(PointRectCollide(mouseP, self.backButtonRect)):
					self.boldRender = 0
				else:
					self.boldRender = -1
			elif(event.type == pygame.MOUSEBUTTONDOWN):
				pygame.mixer.Sound.play(self.menuSelectSound)
				if(PointRectCollide(mouseP,self.backButtonRect)):
					#a mousemotion event at the state change so that highlights can be set
					pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)
					self.subState = 1

	def Render(self, surface):
		#background
		if(not self.stateArgs["night"]): 	surface.blit(self.backG, (0,0))
		else:							surface.blit(self.backGN, (0,0))

		#start
		if(self.subState == 1):
			#game name
	
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 305))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 355))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 405))

			if self.boldRender == 1:
				surface.blit(self.playTextM, (self.playRect[0]+20, self.playRect[1]))
			else:
				surface.blit(self.playText, (self.playRect[0]+20, self.playRect[1]))
			if self.boldRender == 2:
				surface.blit(self.instTextM, (self.instRect[0]+20, self.instRect[1]))
			else:
				surface.blit(self.instText, (self.instRect[0]+20, self.instRect[1]))
			if self.boldRender == 3:
				surface.blit(self.leadTextM, (self.leadRect[0]+20, self.leadRect[1]))
			else:
				surface.blit(self.leadText, (self.leadRect[0]+20, self.leadRect[1]))
			if self.boldRender == 7:
				surface.blit(self.moonImgH, (self.moonRect[0], self.moonRect[1]))
			elif self.stateArgs["night"] == False:
				surface.blit(self.moonImgD, (self.moonRect[0], self.moonRect[1]))
			else:
				surface.blit(self.moonImgS, (self.moonRect[0], self.moonRect[1]))

			if self.boldRender == 8:
				surface.blit(self.speakerImgH, (self.speakerRect[0], self.speakerRect[1]))
			elif self.sound == False:
				surface.blit(self.speakerImgD, (self.speakerRect[0], self.speakerRect[1]))
			else:
				surface.blit(self.speakerImgS, (self.speakerRect[0], self.speakerRect[1]))
		#level choose
		elif (self.subState == 2):
			surface.blit(self.chooseLevelText, (SCREEN_WIDTH/2 - self.chooseLevelText.get_width()/2, SCREEN_HEIGHT/8-30))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 215))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 265))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 315))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 365))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 415))
			if(self.boldRender == 0):
				surface.blit(self.backButtonM, (self.backButtonRect[0],self.backButtonRect[1]))
			else:
				surface.blit(self.backButton, (self.backButtonRect[0], self.backButtonRect[1]))
			if(self.boldRender == 1):
				surface.blit(self.level1TextM, (self.level1Rect[0]+20, self.level1Rect[1]))
			else:
				surface.blit(self.level1Text, (self.level1Rect[0]+20, self.level1Rect[1]))
			if(self.boldRender == 2):
				surface.blit(self.level2TextM, (self.level2Rect[0]+20, self.level2Rect[1]))
			else:
				surface.blit(self.level2Text, (self.level2Rect[0]+20, self.level2Rect[1]))
			if(self.boldRender == 3):
				surface.blit(self.level3TextM, (self.level3Rect[0]+20, self.level3Rect[1]))
			else:
				surface.blit(self.level3Text, (self.level3Rect[0]+20, self.level3Rect[1]))
			if(self.boldRender == 4):
				surface.blit(self.level4TextM, (self.level4Rect[0]+20, self.level4Rect[1]))
			else:
				surface.blit(self.level4Text, (self.level4Rect[0]+20, self.level4Rect[1]))
			if(self.boldRender == 5):
				surface.blit(self.level5TextM, (self.level5Rect[0]+20, self.level5Rect[1]))
			else:
				surface.blit(self.level5Text, (self.level5Rect[0]+20, self.level5Rect[1]))

		#instructions
		elif(self.subState == 3):
			if(self.boldRender == 0):
				surface.blit(self.backButtonM, (self.backButtonRect[0],self.backButtonRect[1]))
			else:
				surface.blit(self.backButton, (self.backButtonRect[0], self.backButtonRect[1]))
			surface.blit(self.scrollBig, (150,150))
			yoffset = 185
			xoffset = 190
			yspacing = 45
			surface.blit(self.line1, (xoffset,yoffset))
			surface.blit(self.line2, (xoffset,yoffset+1*yspacing))
			surface.blit(self.line3, (xoffset,yoffset+2*yspacing))
			surface.blit(self.line4, (xoffset,yoffset+3*yspacing))
			surface.blit(self.line5, (xoffset,yoffset+4*yspacing))

	def Update(self, dT, gsh):
		pass

	def Exit(self):
		pass

class PlaySubStatesEnum() :
	PLAY=0
	PAUSE=1
	HANG=2

class PlayGame(GameState):
	def __init__(self):
		self.SUBSTATES = PlaySubStatesEnum()
		self.RECREATE_PLAYER = pygame.USEREVENT + 1
		self.DISPLAY_STAT = pygame.USEREVENT + 2
		self.COUNTDOWN = pygame.USEREVENT + 3
		self.RESTART_GAME = pygame.USEREVENT + 4
		self.SWITCHTRAPS = pygame.USEREVENT+5
		self.HITRESTORE = pygame.USEREVENT+6
		self.TRANSPORT = pygame.USEREVENT + 7
		self.RESUME_COLLISIONS = pygame.USEREVENT + 8
		self.FIRE_ANIMATION = pygame.USEREVENT + 9
		self.PLAY_STEP_SOUND = pygame.USEREVENT + 10
		

	'''
	Args:
		level, night(True or False)
	'''
	def Enter(self, args):
		self.level=1
		self.phase=0		#for collectible animation
		if "level" in args:		self.level = args["level"]
		self.night = args["night"] if "night" in args else False
		#self.maze = Maze(10, timer=90, ghosts=25, traps=5,trapEvent = self.SWITCHTRAPS, cycles=50, bullets=35)
		match(self.level):
			case(1):
				self.maze = Maze(12, timer=90, ghosts=5, cycles=10, bullets=15, portals=2, trapEvent=self.SWITCHTRAPS)
				self.camera = Camera((500,500),50,(250,250), (-50,-50), (1058, 1058))
			case(2):
				self.maze = Maze(12, timer=85, ghosts=10, traps=5, blocks=5, cycles=7, portals=2, bullets=10, trapEvent=self.SWITCHTRAPS)
				self.camera = Camera((500,500),150,(250,250), (-50,-50), (1058, 1058))
			case(3):
				self.maze = Maze(17, timer=120, ghosts=15, traps=10, blocks=25, bullets=10,portals=3, trapEvent=self.SWITCHTRAPS)
				self.camera = Camera((500,500),150,(250,250), (-50,-50), (1478, 1478))
			case(4):
				self.maze = Maze(20, timer=180, ghosts=15, traps=10, blocks=40, bullets=5,portals=3, trapEvent=self.SWITCHTRAPS)
				self.camera = Camera((500,500),300,(250,250), (-50,-50), (1730, 1730)) 
			case(5):
				self.maze = Maze(12, timer=90, ghosts=25, cycles=48, bullets=25, trapEvent=self.SWITCHTRAPS)
				self.camera = Camera((500,500),250,(250,250), (-50,-50), (1058, 1058))
		self.score = 0
		self.subState = self.SUBSTATES.PLAY
		self.cameraRenderLocation=(390,70)
		self.camera.LoadMedia("res/img/wallLong.png", "res/img/wallShort.png", "res/img/Forest.png", "res/img/grass.png")
		self.camera.CreateMazeImage(self.maze.blockSize+self.maze.wallSize, self.maze.wallSize, self.maze.blockSize, self.maze.size, self.maze.blockedRects, night=self.night)
		
		self.backLayer = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
		for i in range(SCREEN_WIDTH// self.camera.tileOut.get_width() + 1):
			for j in range((SCREEN_HEIGHT // self.camera.tileOut.get_height()) + 1):
				self.backLayer.blit(self.camera.tileOut, (i*self.camera.tileOut.get_width(), j*self.camera.tileOut.get_height()))
		
		#sound
		self.menuSelectSound = pygame.mixer.Sound("res/sound/MenuSelect.mp3")

		self.grayCoverSurface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
		self.grayCoverSurface.fill((0,0,0))
		self.grayCoverSurface.set_alpha(196)

		self.scrollV = pygame.image.load("res/img/scroll_v.png").convert_alpha()
		self.scrollV = pygame.transform.scale(self.scrollV, (300, 250))

		##print("HERE################################################")
		self.scrollH = pygame.image.load("res/img/scroll_h.png").convert_alpha()
		self.scrollH = pygame.transform.scale(self.scrollH, (450, 110))


		fog.init((960,640), [
			(-50,-50,450,690,5000),		#left region
			(330, -20, 60, 650, 400),	#left
			(400,-30,510,90, 1500),		#top
			(400,500,510,140,2000),		#bottom
			(830,-10,140,650,2000)		#right
			])

		buttonImg = pygame.image.load("res/img/single.png").convert_alpha()
		pause = pygame.image.load("res/img/pause.png")
		pause = pygame.transform.scale(pause, (50,50))
		pause.set_colorkey(CLR_KEY)
		self.pauseButton = pygame.transform.scale(buttonImg, (50, 50))
		self.pauseButton.blit(pause, (0, 0))
		self.pauseButtonRect = (25,25,50,50)

		pygame.time.set_timer(self.DISPLAY_STAT, 100, 0)
		pygame.time.set_timer(self.SWITCHTRAPS, 2000, 0)

        #a mousemotion event at the start so that highlights can be set
		pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)

		self.boldRender = -1

		self.mainMenuText = Text.render("Main Menu", "Reg", 30, CLR_BROWN)
		self.resumeText = Text.render("Resume", "Reg", 30, CLR_BROWN)
		self.exitText = Text.render("Exit Game", "Reg", 30, CLR_BROWN)
		self.mainMenuTextM = Text.render("Main Menu", "M", 30, CLR_BROWN)
		self.resumeTextM = Text.render("Resume", "M", 30, CLR_BROWN)
		self.exitTextM = Text.render("Exit Game", "M", 30, CLR_BROWN)

		self.mainMenuRect = (SCREEN_WIDTH/2 - self.mainMenuText.get_width()/2 - 20, 370, self.mainMenuText.get_width()+40, self.mainMenuText.get_height())
		self.resumeRect = (SCREEN_WIDTH/2 - self.resumeText.get_width()/2 - 20, 420, self.resumeText.get_width()+40, self.resumeText.get_height())
		self.exitRect = (SCREEN_WIDTH/2 - self.exitText.get_width()/2 - 20, 470, self.exitText.get_width()+40, self.exitText.get_height())

		#Sprite Objects
		self.portalSpriteObj = PortalSprite("res/img/portal.png")
		self.trapSpriteObj = TrapSprite("res/img/spikes.png")
		self.blockSpriteObj = BlockSprite(["res/img/wall/state" + str(i) + ".png" for i in range(1,4)])

		self.scrollImg = pygame.image.load("res/img/scroll.png").convert_alpha()
		self.scrollImg = pygame.transform.scale(self.scrollImg, (48,48))


	def Render(self, surface):
		surface.blit(self.backLayer, (0,0))
		if(self.subState == self.SUBSTATES.PLAY):
			objects = []
			for g in self.maze.traps:
				gPos = g.GetPosition()
				gDim = (g.w, g.h)
				gI = self.trapSpriteObj.GetImage(g.GetImage())

				objects.append((gPos, gDim, gI))

			for p in self.maze.portals:
				pPos1, pPos2 = p.GetPos1(), p.GetPos2()
				pI = self.portalSpriteObj.GetImage(p.GetImage())
				pDim = (p.w, p.h)
				objects.append((pPos1, pDim, pI))
				objects.append((pPos2, pDim, pI))

			for b in self.maze.bullets:
				bPos = b.GetPosition()
				bI = b.GetImage()
				bDim = (b.w, b.h)
				objects.append((bPos, bDim, bI))

			offset = int(10*(math.sin(self.phase)))
			for c in self.maze.collectibles:
				cPos = c.GetPosition()
				cPos = (cPos[0], cPos[1]+offset)
				cI = c.GetImage()
				cDim = (c.w, c.h)
				objects.append((cPos, cDim, cI))

			#scroll
			sPos = (self.maze.size*self.maze.blockSize-60, self.maze.size*self.maze.blockSize-60)
			sDim = (48,48)
			objects.append((sPos, sDim, self.scrollImg))


			for b in self.maze.blocks:
				bPos = b.GetPosition()
				bDim = (b.w, b.h)
				bI = self.blockSpriteObj.GetImage(b.GetImage())
				objects.append((bPos, bDim, bI))
				##print(bPos)

			for g in self.maze.ghosts:
				gPos = g.GetPosition()
				gDim = (g.w, g.h)
				gI = g.GetImage()
				objects.append((gPos, gDim, gI))


			
			pPos = self.maze.player.GetPosition()
			pDim = (self.maze.player.w, self.maze.player.h)
			pI = self.maze.player.GetImage()
			objects.append((pPos, pDim, pI))

			#render camera
			image = self.camera.GetImage(objects)
			surface.blit(image, self.cameraRenderLocation)

			#render fog
			surface.blit(fog.GetImage(), (0,0))

			surface.blit(self.pauseButton, (self.pauseButtonRect[0], self.pauseButtonRect[1]))

			#render data
			surface.blit(self.scrollV, (100,50))
			if(self.maze.timer>10): time_text = Text.render(f"Time: {round(self.maze.timer)}", "Reg",40, pygame.Color(82,52,14))
			else:					time_text = Text.render(f"Time: {round(self.maze.timer)}", "Reg",40, pygame.Color(255,52,14))
			surface.blit(time_text, (180,100))
			life_text = Text.render(f"Lives: {round(self.maze.lives)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(life_text, (175,180))
			surface.blit(self.scrollV, (100, 350))
			
			score_text = Text.render(f"Score: {round(self.score)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(score_text, (150,400))
			bullets_text = Text.render(f"Spells: {round(self.maze.player.bullets)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(bullets_text, (155,480))
	
		elif(self.subState == self.SUBSTATES.HANG):
			objects = []
			for g in self.maze.traps:
				gPos = g.GetPosition()
				gDim = (g.w, g.h)
				gI = self.trapSpriteObj.GetImage(g.GetImage())

				objects.append((gPos, gDim, gI))

			for p in self.maze.portals:
				pPos1, pPos2 = p.GetPos1(), p.GetPos2()
				pI = self.portalSpriteObj.GetImage(p.GetImage())
				pDim = (p.w, p.h)
				objects.append((pPos1, pDim, pI))
				objects.append((pPos2, pDim, pI))

			for b in self.maze.bullets:
				bPos = b.GetPosition()
				bI = b.GetImage()
				bDim = (b.w, b.h)
				objects.append((bPos, bDim, bI))

			offset = int(10*(math.sin(self.phase)))
			for c in self.maze.collectibles:
				cPos = c.GetPosition()
				cPos = (cPos[0], cPos[1]+offset)
				cI = c.GetImage()
				cDim = (c.w, c.h)
				objects.append((cPos, cDim, cI))

			#scroll
			sPos = (self.maze.size*self.maze.blockSize-60, self.maze.size*self.maze.blockSize-60)
			sDim = (48,48)
			objects.append((sPos, sDim, self.scrollImg))

			for b in self.maze.blocks:
				bPos = b.GetPosition()
				bDim = (b.w, b.h)
				bI = self.blockSpriteObj.GetImage(b.GetImage())
				objects.append((bPos, bDim, bI))

			for g in self.maze.ghosts:
				gPos = g.GetPosition()
				gDim = (g.w, g.h)
				gI = g.GetImage()
				objects.append((gPos, gDim, gI))
			
			pPos = self.maze.player.GetPosition()
			pDim = (self.maze.player.w, self.maze.player.h)
			pI = self.maze.player.GetImage()
			objects.append((pPos, pDim, pI))

			#render camera
			image = self.camera.GetImage(objects)
			surface.blit(image, self.cameraRenderLocation)
			surface.blit(fog.GetImage(), (0,0))

			#render data
			surface.blit(self.scrollV, (100,50))
			time_text = Text.render(f"Time: {round(self.maze.timer)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(time_text, (180,100))
			life_text = Text.render(f"Lives: {round(self.maze.lives)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(life_text, (175,180))
			
			surface.blit(self.scrollV, (100, 350))
			score_text = Text.render(f"Score: {round(self.score)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(score_text, (150,400))
			bullets_text = Text.render(f"Spells: {round(self.maze.player.bullets)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(bullets_text, (155,480))

			#pause button
			surface.blit(self.pauseButton, (self.pauseButtonRect[0], self.pauseButtonRect[1]))

			#countdown
			surface.blit(self.grayCoverSurface, (0,0))
			countdownSurface = Text.render(str(self.countdown), "Reg", 75, (255,200,0))
			surface.blit(countdownSurface, (620, 270))

		elif(self.subState == self.SUBSTATES.PAUSE):
			objects = []
			for g in self.maze.traps:
				gPos = g.GetPosition()
				gDim = (g.w, g.h)
				gI = self.trapSpriteObj.GetImage(g.GetImage())

				objects.append((gPos, gDim, gI))

			for p in self.maze.portals:
				pPos1, pPos2 = p.GetPos1(), p.GetPos2()
				pI = self.portalSpriteObj.GetImage(p.GetImage())
				pDim = (p.w, p.h)
				objects.append((pPos1, pDim, pI))
				objects.append((pPos2, pDim, pI))

			for b in self.maze.bullets:
				bPos = b.GetPosition()
				bI = b.GetImage()
				bDim = (b.w, b.h)
				objects.append((bPos, bDim, bI))

			offset = int(10*(math.sin(self.phase)))
			for c in self.maze.collectibles:
				cPos = c.GetPosition()
				cPos = (cPos[0], cPos[1]+offset)
				cI = c.GetImage()
				cDim = (c.w, c.h)
				objects.append((cPos, cDim, cI))

			#scroll
			sPos = (self.maze.size*self.maze.blockSize-60, self.maze.size*self.maze.blockSize-60)
			sDim = (48,48)
			objects.append((sPos, sDim, self.scrollImg))

			for b in self.maze.blocks:
				bPos = b.GetPosition()
				bDim = (b.w, b.h)
				bI = self.blockSpriteObj.GetImage(b.GetImage())
				objects.append((bPos, bDim, bI))

			for g in self.maze.ghosts:
				gPos = g.GetPosition()
				gDim = (g.w, g.h)
				gI = g.GetImage()
				objects.append((gPos, gDim, gI))
			
			pPos = self.maze.player.GetPosition()
			pDim = (self.maze.player.w, self.maze.player.h)
			pI = self.maze.player.GetImage()
			objects.append((pPos, pDim, pI))

			#render camera
			image = self.camera.GetImage(objects)
			surface.blit(image, self.cameraRenderLocation)
			surface.blit(fog.GetImage(), (0,0))

			#render data
			surface.blit(self.scrollV, (100,50))
			time_text = Text.render(f"Time: {round(self.maze.timer)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(time_text, (180,100))
			life_text = Text.render(f"Lives: {round(self.maze.lives)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(life_text, (175,180))
			surface.blit(self.scrollV, (100, 350))
			
			score_text = Text.render(f"Score: {round(self.score)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(score_text, (150,400))
			bullets_text = Text.render(f"Spells: {round(self.maze.player.bullets)}", "Reg",40, pygame.Color(82,52,14))
			surface.blit(bullets_text, (155,480))

			#pause button
			surface.blit(self.pauseButton, (self.pauseButtonRect[0], self.pauseButtonRect[1]))
			surface.blit(self.grayCoverSurface, (0,0))	

			#Pause Menu
			scrollW = self.scrollH.get_width()
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - scrollW/2, 335))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - scrollW/2, 385))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - scrollW/2, 435))

			if(self.boldRender == 1):
				surface.blit(self.mainMenuTextM, (self.mainMenuRect[0]+20, self.mainMenuRect[1]))
			else:
				surface.blit(self.mainMenuText,  (self.mainMenuRect[0]+20, self.mainMenuRect[1]))
			if(self.boldRender == 2):
				surface.blit(self.resumeTextM, (self.resumeRect[0]+20, self.resumeRect[1]))
			else:
				surface.blit(self.resumeText,  (self.resumeRect[0]+20, self.resumeRect[1]))
			if(self.boldRender == 3):
				surface.blit(self.exitTextM, (self.exitRect[0]+20, self.exitRect[1]))
			else:
				surface.blit(self.exitText,  (self.exitRect[0]+20, self.exitRect[1]))
			
	def Update(self, dT, gsh):
		self.phase += 3*dT
		self.phase %= 2*math.pi
		fog.Update(dT)
		if(self.subState == self.SUBSTATES.PLAY):
			playerAlive = self.maze.Update(dT)
			self.score += self.maze.GetScoreChange() * (3 if self.level == 5 else 1)
			self.score = max(self.score, 0)
			self.maze.timer -= dT
			pPos = self.maze.player.GetCenter()
			self.camera.UpdatePosition(pPos, dT)

			if(not playerAlive):
				self.maze.lives -= 1

			winState = self.maze.CheckWinState()
			if(winState == 1):
				self.score += 300 + round((self.maze.timer ** 1.7 - 100 / max(self.maze.timer, 1) + 100)) + 100*self.maze.lives
				nextState = GS.GAMEOVER
				stateArgs = {'winState': winState, 'score': self.score, 'level': self.level, "night": self.night}
				#print("win###########################################")
				gsh.SetNextState(nextState, stateArgs)
			elif(winState == -1):
				nextState = GS.GAMEOVER
				stateArgs = {'winState': winState, 'level': self.level, "night": self.night}
				#print("lose##########################################")
				gsh.SetNextState(nextState, stateArgs)
			elif(winState==2):
				self.subState = self.SUBSTATES.HANG
				self.maze.bullets.clear()
				#self.maze.CreatePlayer()
				#set a restart game event after 2s
				pygame.time.set_timer(self.RECREATE_PLAYER, 2000, 1)
				pygame.time.set_timer(self.COUNTDOWN, 1000, 4)
				pygame.time.set_timer(self.RESTART_GAME, 5000, 1)
				self.countdown=5

	def EventHandler(self, event, gsh):
		if(self.subState == self.SUBSTATES.PLAY):
			#check mouse clicks
			if(event.type == pygame.MOUSEBUTTONDOWN):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.pauseButtonRect)):
					self.subState = self.SUBSTATES.PAUSE
				
				#mouse click in maze coordinates = mouseP - cameraTopLeft + cameraPo
				cPos = self.camera.GetPosition()
				mX,mY = mouseP[0]-self.cameraRenderLocation[0]+cPos[0], mouseP[1]-self.cameraRenderLocation[1]+cPos[1]
				self.maze.MouseClick((mX,mY))
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_ESCAPE):
					self.subState = self.SUBSTATES.PAUSE
			if(event.type == self.DISPLAY_STAT):
				os.system("clear")
				#print(self.maze.lives, self.maze.timer, self.score)
				#pass

			self.maze.EventHandler(event)

		elif(self.subState == self.SUBSTATES.HANG):
			if(event.type == self.RECREATE_PLAYER):
				self.camera.ResetPosition()
				self.maze.CreatePlayer()
			if(event.type == self.COUNTDOWN):
				self.countdown -= 1
			if(event.type == self.RESTART_GAME):
				self.subState = self.SUBSTATES.PLAY
				pygame.time.set_timer(self.HITRESTORE, 10, 1)
			#handle mouse clicks
			if(event.type == pygame.MOUSEBUTTONDOWN):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.pauseButtonRect)):
					self.subState = self.SUBSTATES.PAUSE
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_ESCAPE):
					self.subState = self.SUBSTATES.PAUSE
   
		#pause
		elif(self.subState == self.SUBSTATES.PAUSE):	
			if(event.type == pygame.MOUSEMOTION):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.mainMenuRect)):
					self.boldRender = 1
				elif(PointRectCollide(mouseP, self.resumeRect)):
					self.boldRender = 2
				elif(PointRectCollide(mouseP, self.exitRect)):
					self.boldRender = 3
				else:
					self.boldRender = -1

			if(event.type == pygame.MOUSEBUTTONDOWN):
				pygame.mixer.Sound.play(self.menuSelectSound)
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.mainMenuRect)):
					gsh.SetNextState(GS.START_SCR, {"night": self.night})
				elif(PointRectCollide(mouseP, self.resumeRect)):
					self.subState = self.SUBSTATES.HANG
					self.countdown = 3
					pygame.time.set_timer(self.COUNTDOWN, 1000, 3)
					pygame.time.set_timer(self.RESTART_GAME, 3000, 1)
				elif(PointRectCollide(mouseP, self.exitRect)):
					pygame.time.set_timer(pygame.QUIT, 10, 1)
				else:
					self.boldRender = -1
	
	def Exit(self):
		self.maze = None
		self.timer = 0
		self.score = 0
		self.subState = self.SUBSTATES.PAUSE
		pygame.time.set_timer(self.DISPLAY_STAT, 0, 0)
		pygame.time.set_timer(self.SWITCHTRAPS, 0, 0)
		fog.Quit()

class GameOver(GameState):
	def __init__(self):
		#sound
		self.menuSelectSound = pygame.mixer.Sound("res/sound/MenuSelect.mp3")

	'''
	Arguments:
		winState: 1 or -1
		score: score
		level: level
	'''
	def Enter(self, args):
		
		self.night = args["night"] if "night" in args else False

		ForestTile = pygame.image.load("res/img/Forest.png")
		self.backLayer = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
		for i in range(SCREEN_WIDTH// ForestTile.get_width() + 1):
			for j in range((SCREEN_HEIGHT // ForestTile.get_height()) + 1):
				self.backLayer.blit(ForestTile, (i*ForestTile.get_width(), j*ForestTile.get_height()))
		
		self.scrollV = pygame.image.load("res/img/scroll_v.png").convert_alpha()
		self.scrollH = pygame.image.load("res/img/scroll_h.png").convert_alpha()

		self.scrollV = pygame.transform.scale(self.scrollV, (485, 400))

		fog.init((SCREEN_WIDTH,SCREEN_HEIGHT), [
			(-50, -50, SCREEN_WIDTH+50, SCREEN_HEIGHT+50, 7000)
			])
		
		self.winState = args["winState"]

		self.score = 0
		if "score" in args:
			self.score = args["score"]

		self.level=1
		if "level" in args:
			self.level=args["level"]

		if(self.winState == 1):
			self.msgText = Text.render("YOU WON!!", "B", 60, pygame.Color(82,52,14))
		else:
			self.msgText = Text.render("YOU LOST", "B", 60, pygame.Color(82,52,14))

		self.BoldRender = 1

		self.playAgainText = Text.render("Play Again", "Reg", 40, pygame.Color(82,52,14))
		self.mainMenuText = Text.render("Main Menu", "Reg", 40, pygame.Color(82,52,14))
		self.leaderBrdText = Text.render("Leaderboard", "Reg", 40, pygame.Color(82,52,14))
		self.playAgainTextM = Text.render("Play Again", "M", 40, pygame.Color(48,29,3))
		self.mainMenuTextM = Text.render("Main Menu", "M", 40, pygame.Color(48,29,3))
		self.leaderBrdTextM = Text.render("Leaderboard", "M", 40, pygame.Color(48,29,3))
		self.saveScoreText = Text.render("Save Score", "Reg", 40, pygame.Color(82,52,14))
		self.saveScoreTextM = Text.render("Save Score", "M", 40, pygame.Color(48,29,3))
		self.textHeight = Text.getHeight("Reg", 40)

		self.PlayAgainRect = (SCREEN_WIDTH/2 - self.scrollV.get_width()/2+50, 6*SCREEN_HEIGHT/16+40, 350, self.textHeight)
		self.MainMenuRect = (SCREEN_WIDTH/2 - self.scrollV.get_width()/2+50, 6*SCREEN_HEIGHT/16+40+1.25*self.textHeight, 350,self.textHeight)
		self.leaderBrdRect = (SCREEN_WIDTH/2 - self.scrollV.get_width()/2+50, 6*SCREEN_HEIGHT/16+40+2.5*self.textHeight, 350, self.textHeight)
		self.saveScoreRect = (SCREEN_WIDTH/2 - self.scrollV.get_width()/2+50, 6*SCREEN_HEIGHT/16+40+3.75*self.textHeight, 350, self.textHeight)

		#a mousemotion event at the start so that highlights can be set
		pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)
	def Update(self, dT, gsh):
		pass

	def Render(self, surface):
		surface.blit(self.backLayer, (0,0))
		surface.blit(fog.GetImage(), (0,0))

		scrollH = pygame.transform.scale(self.scrollH, (600, 300))
		surface.blit( scrollH, (SCREEN_WIDTH/2 - scrollH.get_width()/2, 2*SCREEN_HEIGHT/16 - scrollH.get_height()/2 + 40))
		surface.blit(self.msgText, (SCREEN_WIDTH/2 - self.msgText.get_width()/2, 2*SCREEN_HEIGHT/16 - self.msgText.get_height()/2 + 50))

		scoreText = Text.render(f"Score: {self.score}", "Reg", 25, pygame.Color(82,52,14))
		if(self.winState == 1):
			scrollH = pygame.transform.scale(self.scrollH, (200, 120))
			surface.blit(scrollH, (SCREEN_WIDTH/2 - scrollH.get_width()/2, 3*SCREEN_HEIGHT/16))
			surface.blit(scoreText, (SCREEN_WIDTH/2 - scoreText.get_width()/2, 3*SCREEN_HEIGHT/16+45))

		surface.blit(self.scrollV, (SCREEN_WIDTH/2 - self.scrollV.get_width()/2, 6 * SCREEN_HEIGHT/16))
		if self.BoldRender == 0:
			surface.blit(self.playAgainTextM, (self.PlayAgainRect[0], self.PlayAgainRect[1]))
		else:
			surface.blit(self.playAgainText, (self.PlayAgainRect[0], self.PlayAgainRect[1]))
		if self.BoldRender == 1:
			surface.blit(self.mainMenuTextM, (self.MainMenuRect[0], self.MainMenuRect[1]))
		else:
			surface.blit(self.mainMenuText, (self.MainMenuRect[0], self.MainMenuRect[1]))
		if self.BoldRender == 2:
			surface.blit(self.leaderBrdTextM, (self.leaderBrdRect[0], self.leaderBrdRect[1]))
		else:
			surface.blit(self.leaderBrdText, (self.leaderBrdRect[0], self.leaderBrdRect[1]))
		
		if(self.winState == 1):
			if self.BoldRender == 3:
				surface.blit(self.saveScoreTextM, (self.saveScoreRect[0], self.saveScoreRect[1]))
			else:
				surface.blit(self.saveScoreText, (self.saveScoreRect[0], self.saveScoreRect[1]))

	def EventHandler(self, event, gsh: GameStateHandler):
		if(event.type == pygame.MOUSEMOTION):
			mouseP = pygame.mouse.get_pos()
			if PointRectCollide(mouseP, self.PlayAgainRect):
				self.BoldRender = 0
			elif PointRectCollide(mouseP, self.MainMenuRect):
				self.BoldRender = 1
			elif PointRectCollide(mouseP, self.leaderBrdRect):
				self.BoldRender = 2
			elif PointRectCollide(mouseP, self.saveScoreRect):
				self.BoldRender = 3
			else:
				self.BoldRender = -1
		elif(event.type == pygame.MOUSEBUTTONDOWN):
			pygame.mixer.Sound.play(self.menuSelectSound)
			mouseP = pygame.mouse.get_pos()
			if PointRectCollide(mouseP, self.PlayAgainRect):
				gsh.SetNextState(GS.PLAY_GAME, {"level": self.level, "night": self.night})
			elif PointRectCollide(mouseP, self.MainMenuRect):
				gsh.SetNextState(GS.START_SCR, {"night": self.night})
			elif PointRectCollide(mouseP, self.leaderBrdRect):
				gsh.SetNextState(GS.LEADER_BRD, {"level": self.level, "night": self.night})
			elif PointRectCollide(mouseP, self.saveScoreRect):
				if(self.winState == 1):	gsh.SetNextState(GS.SAVE_SCORE, {"score": self.score, "level": self.level, "night": self.night})

	def Exit(self):
		fog.Quit()

class SaveScore(GameState):
	def __init__(self):
		pass

	def Enter(self, args):
		if("score" not in args):
			#print("ArgumentError: Save Score called without score argument")
			assert(False)
		else:
			self.score = args["score"]

		if("level" not in args):
			#print("ArgumentError: Save Score called without level argument")
			assert(False)
		else:
			self.level = args["level"]
		
		self.night = args["night"] if "night" in args else False
		
		self.name = ""

		self.backgroundImg = pygame.image.load("res/img/backg.png").convert_alpha()
		self.backgroundImgN = pygame.image.load("res/img/backgN.png").convert_alpha()

		self.textBox = pygame.image.load("res/img/scroll_mod.png").convert_alpha()
		self.textBox = pygame.transform.scale(self.textBox, (600, 70))
		self.textBoxRect = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2-120, 600, 70)

		self.scrollH = pygame.image.load("res/img/scroll_h.png").convert_alpha()
		self.scrollH = pygame.transform.scale(self.scrollH, (300, 120))
		self.saveText = Text.render("Save", "Reg", 30, CLR_BROWN)
		self.saveTextM = Text.render("Save", "B", 30, CLR_BROWN)
		self.saveRect = (SCREEN_WIDTH/2 - self.saveText.get_width()/2-20, 3*SCREEN_HEIGHT/4, self.saveText.get_width()+40, self.saveText.get_height())

		self.boldRender = 1

		self.enterNameText = Text.render("Enter You Name", "Reg", 40, CLR_BROWN)

		#sound
		self.menuSelectSound = pygame.mixer.Sound("res/sound/MenuSelect.mp3")

		#a mousemotion event at the start so that highlights can be set
		pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)
	
	def Render(self, surface):
		if(not self.night):	surface.blit(self.backgroundImg, (0,0))
		else:				surface.blit(self.backgroundImgN, (0,0))
		surface.blit(self.textBox,(self.textBoxRect[0]-self.textBoxRect[2]/2, self.textBoxRect[1]-self.textBoxRect[3]/2))
		surface.blit(self.enterNameText, (self.textBoxRect[0]-self.enterNameText.get_width()/2, self.textBoxRect[1]-self.textBoxRect[3]/2-100))
		text = Text.render(self.name, "Reg", 40, CLR_BROWN)
		surface.blit(text, (self.textBoxRect[0] - text.get_width()/2, self.textBoxRect[1]-text.get_height()/2))

		surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 3*SCREEN_HEIGHT/4-40))
		if(self.boldRender == 1):
			surface.blit(self.saveTextM, (self.saveRect[0]+20, self.saveRect[1]))
		else:
			surface.blit(self.saveText, (self.saveRect[0]+20, self.saveRect[1]))

	def EventHandler(self, event, gsh):
		if(event.type == pygame.KEYDOWN):
			if event.key == pygame.K_RETURN:
				if(len(self.name)>0):
					data = ReadScoreFile(f"files/scores/level{self.level}.txt")
					data.append((self.name, self.score))
					writeToFile(f"files/scores/level{self.level}.txt", data, 6)
					gsh.SetNextState(GS.LEADER_BRD, {"level": self.level, "night": self.night})
			elif event.key == pygame.K_BACKSPACE:
				self.name = self.name[:-1]
			else:
				self.name += event.unicode

			if(len(self.name) > 10): self.name = self.name[:10]
		elif(event.type == pygame.MOUSEMOTION):
			mouseP = pygame.mouse.get_pos()
			if(PointRectCollide(mouseP, self.saveRect)):
				#print("here")
				self.boldRender = 1
			else:
				#print("over here")
				self.boldRender = -1
		elif(event.type == pygame.MOUSEBUTTONDOWN):
			pygame.mixer.Sound.play(self.menuSelectSound)
			mouseP = pygame.mouse.get_pos()
			if(PointRectCollide(mouseP, self.saveRect)):
				if(len(self.name)>0):
					data = ReadScoreFile(f"files/scores/level{self.level}.txt")
					data.append((self.name, self.score))
					writeToFile(f"files/scores/level{self.level}.txt", data, 6)
					gsh.SetNextState(GS.LEADER_BRD, {"level": self.level, "night": self.night})
			

	def Update(self,dT,gsh):
		pass

	def Exit(self):
		pass

class LeaderBoard(GameState):
	'''
	Substates:
		0 - choose
		1 - display
	'''
	def __init__(self):
		pass
	
	def Enter(self, args):
		self.subState = 0
		self.level = 0
		if("level" in args):
			self.level = args["level"]
			self.subState = 1
			#print("level",self.level)

		self.night = args["night"] if "night" in args else False

		self.backg = pygame.image.load("res/img/backg.png").convert_alpha()
		self.backgN = pygame.image.load("res/img/backgN.png").convert_alpha()
		
		scrollV = pygame.image.load("res/img/scroll_v.png").convert_alpha()
		sH = 480
		sW = 720
		self.scrollV = pygame.transform.scale(scrollV,(sW, sH))
		self.scrollRect = (SCREEN_WIDTH/2 - sW/2 , SCREEN_HEIGHT/2 - sH/2, sW, sH)

		self.scrollH = pygame.image.load("res/img/scroll_h.png").convert_alpha()
		self.scrollH = pygame.transform.scale(self.scrollH, (450, 110))

		#1 to 5: levels
        #0: backButton
		self.boldRender = -1

		#sound
		self.menuSelectSound = pygame.mixer.Sound("res/sound/MenuSelect.mp3")

		self.chooseLevelText = Text.render("Choose a Level", "B", 60, CLR_BROWN)

		self.level1Text = Text.render("Level1", "Reg", 30, CLR_BROWN)
		self.level2Text = Text.render("Level2", "Reg", 30, CLR_BROWN)
		self.level3Text = Text.render("Level3", "Reg", 30, CLR_BROWN)
		self.level4Text = Text.render("Level4", "Reg", 30, CLR_BROWN)
		self.level5Text = Text.render("Bonus Level", "Reg", 30, CLR_BROWN)
		self.level1TextM = Text.render("Level1", "M", 30, CLR_BROWN)
		self.level2TextM = Text.render("Level2", "M", 30, CLR_BROWN)
		self.level3TextM = Text.render("Level3", "M", 30, CLR_BROWN)
		self.level4TextM = Text.render("Level4", "M", 30, CLR_BROWN)
		self.level5TextM = Text.render("Bonus Level", "M", 30, CLR_BROWN)

		self.level1Rect = (SCREEN_WIDTH/2 - self.level1Text.get_width()/2-20, 250, self.level1Text.get_width()+40, self.level1Text.get_height())
		self.level2Rect = (SCREEN_WIDTH/2 - self.level2Text.get_width()/2-20, 300, self.level2Text.get_width()+40, self.level2Text.get_height())
		self.level3Rect = (SCREEN_WIDTH/2 - self.level3Text.get_width()/2-20, 350, self.level3Text.get_width()+40, self.level3Text.get_height())
		self.level4Rect = (SCREEN_WIDTH/2 - self.level4Text.get_width()/2-20, 400, self.level4Text.get_width()+40, self.level4Text.get_height())
		self.level5Rect = (SCREEN_WIDTH/2 - self.level5Text.get_width()/2-20, 450, self.level5Text.get_width()+40, self.level5Text.get_height())
		
		backButton = pygame.image.load("res/img/small.png").convert_alpha()
		backText = Text.render("Main Menu", "Reg", 20, CLR_BROWN)
		backTextM = Text.render("Main Menu", "M", 20, CLR_BROWN)
		self.backButton = pygame.transform.scale(backButton, (155, 50))
		self.backButtonM = pygame.transform.scale(backButton, (155, 50))
		self.backButton.blit(backText, (20,10))
		self.backButtonM.blit(backTextM, (20,10))
		self.backButtonRect = (35, 35, 155, 50)

		#a mousemotion event at the start so that highlights can be set
		pygame.time.set_timer(pygame.MOUSEMOTION, 5, 1)


		self.data =[]
		if(self.level != 0):
			self.data=ReadScoreFile(f"files/scores/level{self.level}.txt")[:5]
		self.dataSurface = None
		
		
	def EventHandler(self, event, gsh):
		if(self.subState == 0):
			if(event.type == pygame.MOUSEMOTION):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.level1Rect)):
					self.boldRender = 1
				elif(PointRectCollide(mouseP, self.level2Rect)):
					self.boldRender = 2
				elif(PointRectCollide(mouseP, self.level3Rect)):
					self.boldRender = 3
				elif(PointRectCollide(mouseP, self.level4Rect)):
					self.boldRender = 4
				elif(PointRectCollide(mouseP, self.level5Rect)):
					self.boldRender = 5
				elif(PointRectCollide(mouseP, self.backButtonRect)):
					self.boldRender = 0
				else:
					self.boldRender = -1
			elif(event.type == pygame.MOUSEBUTTONDOWN):
				pygame.mixer.Sound.play(self.menuSelectSound)
				stateArgs = {"level": 0}
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.level1Rect)):
					self.level = 1
				elif(PointRectCollide(mouseP, self.level2Rect)):
					self.level = 2
				elif(PointRectCollide(mouseP, self.level3Rect)):
					self.level = 3
				elif(PointRectCollide(mouseP, self.level4Rect)):
					self.level = 4
				elif(PointRectCollide(mouseP, self.level5Rect)):
					self.level = 5
				elif(PointRectCollide(mouseP, self.backButtonRect)):
					gsh.SetNextState(GS.START_SCR, {"night": self.night})
				else:
					self.boldRender = -1
				
				if(self.level != 0):
					self.data = ReadScoreFile(f"files/scores/level{self.level}.txt")[:5]
					#print(self.data)
					self.subState = 1
		elif(self.subState==1):
			if(event.type == pygame.MOUSEMOTION):
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.backButtonRect)):
					self.boldRender = 0
				else:
					self.boldRender = -1
			elif(event.type == pygame.MOUSEBUTTONDOWN):
				pygame.mixer.Sound.play(self.menuSelectSound)
				mouseP = pygame.mouse.get_pos()
				if(PointRectCollide(mouseP, self.backButtonRect)):
					gsh.SetNextState(GS.START_SCR, {"night": self.night})
				else:
					self.boldRender = -1




	def Render(self, surface):
		if(self.night): surface.blit(self.backgN, (0, 0))
		else:			surface.blit(self.backg, (0, 0))
		if(self.boldRender == 0):
			surface.blit(self.backButtonM, (self.backButtonRect[0],self.backButtonRect[1]))
		else:
			surface.blit(self.backButton, (self.backButtonRect[0], self.backButtonRect[1]))
		if(self.subState == 0):
			surface.blit(self.chooseLevelText, (SCREEN_WIDTH/2 - self.chooseLevelText.get_width()/2, SCREEN_HEIGHT/8-30))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 215))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 265))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 315))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 365))
			surface.blit(self.scrollH, (SCREEN_WIDTH/2 - self.scrollH.get_width()/2, 415))

			if(self.boldRender == 1):
				surface.blit(self.level1TextM, (self.level1Rect[0]+20, self.level1Rect[1]))
			else:
				surface.blit(self.level1Text, (self.level1Rect[0]+20, self.level1Rect[1]))
			if(self.boldRender == 2):
				surface.blit(self.level2TextM, (self.level2Rect[0]+20, self.level2Rect[1]))
			else:
				surface.blit(self.level2Text, (self.level2Rect[0]+20, self.level2Rect[1]))
			if(self.boldRender == 3):
				surface.blit(self.level3TextM, (self.level3Rect[0]+20, self.level3Rect[1]))
			else:
				surface.blit(self.level3Text, (self.level3Rect[0]+20, self.level3Rect[1]))
			if(self.boldRender == 4):
				surface.blit(self.level4TextM, (self.level4Rect[0]+20, self.level4Rect[1]))
			else:
				surface.blit(self.level4Text, (self.level4Rect[0]+20, self.level4Rect[1]))
			if(self.boldRender == 5):
				surface.blit(self.level5TextM, (self.level5Rect[0]+20, self.level5Rect[1]))
			else:
				surface.blit(self.level5Text, (self.level5Rect[0]+20, self.level5Rect[1]))
		elif(self.subState == 1):
			surface.blit(self.scrollV, (self.scrollRect[0], self.scrollRect[1]))

			if(self.dataSurface == None):
				self.dataSurface = pygame.Surface((self.scrollRect[2], self.scrollRect[3]), pygame.SRCALPHA)
				self.dataSurface.fill((0,0,0,0))
				#transparent = pygame.Surface((self.scrollRect[2], self.scrollRect[3]))
				#transparent.set_alpha
	
				for idx,tup in enumerate(self.data):
					name,score = tup
					idx+=1
					idxImg = Text.render(str(idx), "Reg", 30, CLR_BROWN)
					nameImg = Text.render(str(name), "Reg", 30, CLR_BROWN)
					scoreImg = Text.render(str(score), "Reg", 30, CLR_BROWN)
					height = idxImg.get_height()
					self.dataSurface.blit(idxImg,    (60, 50+(height+20)*(idx-1)))
					self.dataSurface.blit(nameImg,  (160, 50+(height+20)*(idx-1)))
					self.dataSurface.blit(scoreImg, (600, 50+(height+20)*(idx-1)))

			surface.blit(self.dataSurface, (self.scrollRect[0], self.scrollRect[1]))


	def Update(self, dT, gsh):
		pass

	def Exit(self):
		pass