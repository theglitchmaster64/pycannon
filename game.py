import numpy

class Cell:

	def __init__(self,x,y,data=None):
		self.data = data
		self.x = x
		self.y = y

	def __repr__(self):
		return '{0}:({1},{2})'.format(self.data,self.x,self.y)


class Game:

	def __init__(self):
		self.turn = 'red'
		self.board = numpy.empty((10,10), dtype=object)
		for i in range(0,10):
			for j in range(0,10):
				self.board[i][j] = Cell(i,j)
				if (i>=1 and i<=3):
					if j%2 == 1:
						self._setcell(Cell(i,j,data='XXXX'))
				if (i>=6 and i<=8):
					if j%2 == 0:
						self._setcell(Cell(i,j,data='YYYY'))
		print('game ready for player red!')

	def turn_over(self):
		if self.turn == 'red':
			self.turn = 'blue'
		else:
			self.turn = 'red'

	def _setcell(self,cell):
		if (cell.x > 9 or cell.x < 0) or (cell.y > 9 or cell.y < 0):
			print('invalid position for cell!')
			return False
		else:
			self.board[cell.x, cell.y] = cell
			return True


	def __repr__(self):
		retstr = 'turn:{}\nboard:\n'.format(self.turn)
		for i in range(0,10):
			for j in range(0,10):
				retstr += str(self.board[i][j]) + '  '
			retstr += '\n'
		return retstr
