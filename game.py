import numpy


class Cell:

	def __init__(self,x,y,data=0):
		self.data = data
		self.x = x
		self.y = y

	def __repr__(self):
		return '{0}:({1},{2})'.format(self.data,self.x,self.y)


class Game:

	def __init__(self):
		self.turn = 'X'
		self.board = numpy.empty((10,10), dtype=object)
		for i in range(0,10):
			for j in range(0,10):
				self.board[i][j] = Cell(i,j)
				if (i>=1 and i<=3):
					if j%2 == 1:
						self._setcell(Cell(i,j,data='X'))
				if (i>=6 and i<=8):
					if j%2 == 0:
						self._setcell(Cell(i,j,data='Y'))
		print('game ready for player red!')

	def _turn_over(self):
		if self.turn == 'X':
			self.turn = 'Y'
		else:
			self.turn = 'X'

	def _setcell(self,cell):
		if (cell.x > 9 or cell.x < 0) or (cell.y > 9 or cell.y < 0):
			return False
		else:
			self.board[cell.x, cell.y] = cell
			return True

	def move(self,x1,y1,x2,y2):
		valid = False
		c1 = self.board[x1][y1]
		c2 = self.board[x2][y2]
		if c1 == c2:
			return False
		if c1.data != self.turn:
			return False
		elif (c1.data == 0 or c2.data != 0):
			return False
		else:
			if self.turn == 'X':
				newX = c1.x + 1
				newY = [x for x in range(c1.y-1, c1.y+2)]
			else:
				newX = c1.x - 1
				newY = [x for x in range(c1.y-1, c1.y+2)]
			for y in newY:
				if (x2,y2) == (newX,y):
					valid = True
			if valid:
				self._setcell(Cell(c1.x,c1.y,data=0))
				self._setcell(Cell(c2.x, c2.y, data=c1.data))
				self._turn_over()
				return True
			else:
				return False

	def capture(self,x1,y1,x2,y2):
		valid = False
		c1 = self.board[x1][y1]
		c2 = self.board[x2][y2]
		if c1 == c2:
			return False
		if c1.data != self.turn:
			return False
		elif (c1.data == 0 or c2.data == 0):
			return False
		else:
			if self.turn == 'X':
				newX = [x for x in range(c1.x,c1.x+2)]
				newY = [x for x in range(c1.y-1, c1.y+2)]
			else:
				newX = [x for x in range(c1.x-1,c1.x+1)]
				newY = [x for x in range(c1.y-1, c1.y+2)]
			for x in newX:
				for y in newY:
					if (x2,y2) == (x,y):
						valid = True
			if valid:
				self._setcell(Cell(c1.x,c1.y,data=0))
				self._setcell(Cell(c2.x,c2.y,data=c1.data))
				self._turn_over()
				return True
			else:
				return False


	def __repr__(self):
		retstr = 'turn:{}\nboard:\n'.format(self.turn)
		for i in range(0,10):
			for j in range(0,10):
				retstr += str(self.board[i][j]) + '  '
			retstr += '\n'
		return retstr
