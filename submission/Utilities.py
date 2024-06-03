#Utilities Module
#Various classes and methods used throughout the game

import pygame
import math
import os

#A class to store a sprite sheet and get different frames of the sprite sheet
class SpriteSheet:
	#initialize the sprite sheet and load the image into a surface
	#argument: image_path-path of spritesheet image
	def __init__(self, image_path):
		self.spriteSheet = pygame.image.load(image_path)
	
	'''
	get a frame from the sprite sheet
	returns a pygame surface containing the image
	arguments:
		height: height of frame
		width: width of frame
		frame: count of frame to get
	'''
	def getFrame(self, height, width, frame):
		image = pygame.Surface((width, height)).convert_alpha()
		image.fill((0,0,0,0))
		image.blit(self.spriteSheet, (0,0), (width*frame, 0, width, height))
		return image
	
class Vec2:
	def __init__(self,x,y):
		self.x=x
		self.y=y


	def __add__(self, b):
		return Vec2(self.x + b.x, self.y + b.y)
	
	def __sub__(self, b):
		return Vec2(self.x - b.x, self.y - b.y)
	
	def scalarMul(self, k):
		return Vec2(self.x * k, self.y * k)
	
	def __mul__(self, b):
		if(type(b) == Vec2):
			return (self.x*b.x + self.y*b.y)
		else:
			return Vec2(self.x * b, self.y * b)
		
	def abs(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
	
	def __str__(self):
		return f"({self.x}, {self.y})"
	
	def __eq__(self, b):
		return (self.x==b.x and self.y == b.y)

def normalize(a : Vec2):
	if(abs(a.x) != 0 or abs(a.y) != 0):
		norm = math.sqrt(a.x**2 + a.y**2)
	else:
		norm = 1.0
	return Vec2(a.x / norm, a.y / norm)

def vround(a: Vec2):
	return Vec2(round(a.x), round(a.y))

#Enum for Direction
class DirEnum:
	UP = 0
	RIGHT = 1
	LEFT = 2
	DOWN = 3
	NONE = 4

'''
Checks whether two rectangles collide
Arguments:
	two rectangles given as (x,y,w,h)
'''
def RectCollide(rect1, rect2):
	x1,y1,w1,h1 = rect1
	x2,y2,w2,h2 = rect2
	Rect1 = pygame.Rect(x1,y1,w1,h1)
	Rect2 = pygame.Rect(x2,y2,w2,h2)
	return pygame.Rect.colliderect(Rect1, Rect2)
	

'''
Checks whether point is inside rectangle
Arguments:
	pt: (x,y)
	rect: (x,y,w,h)
'''
def PointRectCollide(pt, rect):
	x1,y1=pt
	x2,y2,w,h = rect
	return (x1 > x2 and y1 > y2 and x1 < x2+w and y1 < y2+h)

	


DIR = DirEnum()

'''
returns index of element in list
if element not in list, returns len(list)
'''
def ListFind(list, key):
	for i,v in enumerate(list):
		if v == key:
			return i
	return len(list)

class DisjointSet:
	def __init__(self, n: int):
		self.arr = [i for i in range (n)]
		self.rank = [0 for i in range (n)]
		self.size = n
	
	def find(self, n: int):
		i = n
		j = self.arr[n]
		while(j != i):
			i = j
			j = self.arr[i]
		return j
	
	def union(self, a:int, b:int):
		ap = self.find(a)
		bp = self.find(b)
		if(self.rank[ap] > self.rank[bp]):
			self.arr[ap] = bp
			self.rank[bp] = max(self.rank[bp], self.rank[ap]+1)
		else:
			self.arr[bp] = ap
			self.rank[ap] = max(self.rank[ap], self.rank[bp]+1)

'''
find a path in graph from u to v
Arguments
	u:source
	v:destination
	size:size of graph
	adjList:adjacency list
Return:
	path consisting if vertex indices from source to dest

'''
def FindPath(u:int, v:int,size:int,adjList):
	assert u < size
	assert v < size

	BFSqueue = []
	prev = [-1 for i in range(size)]
	BFSqueue.append(u)
	while(len(BFSqueue)>0):
		i = BFSqueue.pop(0)
		for j in adjList[i]:
			if prev[j] == -1:
				prev[j] = i
				BFSqueue.append(j)
				if(j == v):
					break
	
	path = [v]
	i=v
	while(i!=u):
		i = prev[i]
		path.append(i)
		if(len(path)>size):
			break
	
	path.reverse()
	return path

'''
Arguments:
path: path
adj: adjacency list
size, maze size
'''
def SavePath(path: list, adj:list, size: int):
	def GetRelDir(u,v):
		if(v == u+1):
			return 'R'
		elif(v == u-1):
			return 'L'
		elif (v ==u+size):
			return 'D'
		elif(v == u - size):
			return 'U'
		else:
			return 'P'
	str = ""
	str += GetRelDir(path[0],path[1])
	for i in range(1,len(path)-1):
		#if(len(adj[path[i]]) > 2):
		str += GetRelDir(path[i], path[i+1])
	file = open("solution.txt", 'w')
	file.write(str)
	file.close()

def SmoothingFunction(a, min, max, center, dev):
	aM = (a-center)/dev
	if(aM < -1):	fBase = -1
	elif(aM > 1):   fBase = 1
	elif(aM > 0):
		fBase = 1 - (aM-1)**2
	else:
		fBase = (aM + 1)**2 - 1
	return fBase*((max-min)/2) + (max+min)/2

"""Read scores from csv file"""
def ReadScoreFile(file):
	try:
		file = open(file, "r")
	except FileNotFoundError:
		os.system(f"touch {file}")
		file = open(file, "r")
	data = []
	for l in file:
		if ("," not in l):
			continue
		name, score = l.strip().split(",")
		data.append((name,int(score)))
	file.close()
	data = sorted(data, key=lambda x:-x[1])
	return data

"""
Write Scores to csv file
data: list of tuples (name, data)
max: max no. of entries stored
"""
def writeToFile(file, data, max):
	data = sorted(data, key=lambda x:-x[1])[:max]
	try:
		file = open(file, "w")
	except FileNotFoundError:
		os.system(f"touch {file}")
		file = open(file, "w")
	for l in data:
		file.write(f"{l[0]},{l[1]}\n")
	file.close()
