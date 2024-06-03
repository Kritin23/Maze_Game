import GameState
import pygame

from Player import *
from Utilities import *
from Maze import Maze
from GameState import *
from Camera import Camera
import Text

#Application Class
#Contains Game Window variables such as surface, screen_width, screen_height
#Contains a game state handler object
#implements game loop in RunGSH function
class Application:
	SCREEN_HEIGHT = 640
	SCREEN_WIDTH = 960

	def __init__(self, musicPath, night):
		pygame.mixer.pre_init(44100, -16, 1, 256)
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		pygame.mixer.music.load(musicPath)
		pygame.mixer.music.play(loops=-1)
		self.night = night
		Text.init()
		Text.add("res/fonts/Cinzel-Regular.ttf", 75, "Reg")
		Text.add("res/fonts/Cinzel-Regular.ttf", 40, "Reg")
		Text.add("res/fonts/Cinzel-Regular.ttf", 25, "Reg")
		Text.add("res/fonts/Cinzel-Regular.ttf", 30, "Reg")
		Text.add("res/fonts/Cinzel-Regular.ttf", 20, "Reg")
		Text.add("res/fonts/Cinzel-Medium.ttf", 30, "M")
		Text.add("res/fonts/Cinzel-Medium.ttf", 40, "M")
		Text.add("res/fonts/Cinzel-Medium.ttf", 20, "M")
		Text.add("res/fonts/Cinzel-SemiBold.ttf", 60, "B")
		Text.add("res/fonts/Cinzel-SemiBold.ttf", 30, "B")
		self.gameSurface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
		pygame.display.set_caption("Maze Game")
		self.clock = pygame.time.Clock()
		self.running = False
		self.gsh = GameStateHandler(GS.NONE, {})

	def RunGSH(self):
		self.running = True
		self.gsh.SetNextState(GS.START_SCR, {"night": self.night})
		self.gsh.UpdateState()
		while(self.running):
			#clear screen
			self.gameSurface.fill((0,0,0), None)
			prevFrameTime = self.clock.get_time() / 1000

			for event in pygame.event.get():
				if(event.type == pygame.QUIT):
					self.running = False
					self.gsh.Exit()
					break
				self.gsh.EventHandler(event)
			if( not self.running):	break
			#print("fps: ",self.clock.get_fps())
			self.gsh.Update(prevFrameTime)
			self.gsh.Render(self.gameSurface)

			pygame.display.update()
			self.gsh.UpdateState()
			self.clock.tick(40)
			
	def Test(self):
		self.running=True
		maze = Maze(10, cycles=4)

		camera = Camera(400, 400, 1000, 1000, 200,200)
		camera.LoadMedia("res/img/wallLong.png", "res/img/wallShort.png", "res/img/Forest.png", "res/img/grass.png")
		camera.CreateMazeImage(maze.blockSize+maze.wallSize, maze.wallSize, maze.blockSize, maze.size, maze.blockedRects)

		self.gameSurface.blit(camera.BaseLayer, (0,0))
		self.gameSurface.blit(camera.ShadowLayer, (0,0))
		self.gameSurface.blit(camera.WallLayer, (0,0))
		pygame.display.update()
		while(True):
			pass



	def Exit(self):
		self.running = False
		pygame.font.quit()
		pygame.quit()
