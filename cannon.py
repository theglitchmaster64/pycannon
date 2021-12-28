import numpy as np
import random
import copy

#childs coz childeren is annoying to type

class Board:
	def __init__(self):
		self.matrix = np.empty((10,10),dtype=object)
		for i in range(0,10):
			for j in range(0,10):
				self.matrix[i][j] = '0'
				if (i>=1 and i<=3):
					if j%2 == 1:
						self.matrix[i][j] = 'x'
				if (i>=6 and i<=8):
					if j%2 == 0:
						self.matrix[i][j] = 'y'

	def getpos(self,pos):
		if 0<pos[1]<9 and 0<pos[0]<9:
			return self.matrix[pos[0]][pos[1]]
		else:
			return False

	def setpos(self,pos,data):
		try:
			self.matrix[pos[0]][pos[1]] = data
			return True
		except:
			return False

	def copy(self):
		return copy.deepcopy(self.matrix)

class Player:
	def __init__(self,label,board):
		self.txt = label
		self.board = board
		self.score = 0
		self.pieces = []
		self.town = None
		for i in range(10):
			for j in range(10):
				if self.board.getpos((i,j)) == self.txt:
					self.pieces.append((i,j))

	def place_town(self,pos):
		if (pos[0] == 0) and (0 < pos[1] < 9):
			self.board.setpos((pos),self.txt.upper())
			return True
		elif (pos[0] == 9) and (0 < pos[1] < 9):
			self.board.setpos((pos),self.txt.upper())
			return True
		else:
			return False
