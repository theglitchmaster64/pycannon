import numpy
import copy

class Cell:

	def __init__(self,x,y,data=0):
		self.data = data
		self.x = x
		self.y = y

	def fixup(self):
		if self.x > 9 or self.x < 0:
			self.x = -99999
		elif self.y > 9 or self.y < 0:
			self.y = -99999

	def __repr__(self):
		return '{0}:({1},{2})'.format(self.data,self.x,self.y)


class Game:

	def __init__(self):
		self.turn = 1
		self.board = numpy.empty((10,10), dtype=object)
		self.board_backup = copy.deepcopy(self.board)
		for i in range(0,10):
			for j in range(0,10):
				self.board[i][j] = Cell(i,j)
				if (i>=1 and i<=3):
					if j%2 == 1:
						self._setcell(Cell(i,j,data=+1))
				if (i>=6 and i<=8):
					if j%2 == 0:
						self._setcell(Cell(i,j,data=-1))
		print('game ready for player red!')

	def eval_board(self):
		score = 0
		xp = 0
		yp = 0
		for i in range(0,10):
			for j in range(0,10):
				tmp = self.board[i][j]
				if tmp.data == 1:
					score += 3
					xp += 1
				elif tmp.data == -1:
					score -= 3
					yp += 1
				elif tmp.data == 'X':
					score += 1000
				elif tmp.data == 'Y':
					score -= 1000
				else:
					score += 0
				if (xp == 0):
					score += 1000
				elif (yp == 0):
					score -= 1000
		return score

	def is_game_over(self):
		score = self.eval_board()
		if score > 1000 or score < 1000:
			return True
		else:
			return False

	def set_town(self,n):
		if self.turn == 1:
			self._setcell(Cell(0,n,data='X'))
		else:
			self._setcell(Cell(9,n,data='Y'))
		self._turn_over()

	def _turn_over(self):
		self.turn = -self.turn

	def _setcell(self,cell):
		if (cell.x > 9 or cell.x < 0) or (cell.y > 9 or cell.y < 0):
			return False
		else:
			self.board[cell.x, cell.y] = cell
			return True


	def valid_moves(self,x,y):
		c = self.board[x][y]
		move = []
		shoot = []
		if c.data == 0:
			return []
		elif c.data == +1:
			#move
			newX = [c.x + 1]
			newY = [c.y - 1, c.y, c.y + 1]
		elif c.data == -1:
			#move
			newX = [c.x - 1]
			newY = [c.y - 1, c.y, c.y + 1]
		for i in newX:
			for j in newY:
				if (i,j) != (x,y) and self.board[i][j].data == 0:
					move.append((i,j))
		return move

	def valid_captures(self,x,y):
		c = self.board[x][y]
		capture = []
		if c.data == 0:
			return []
		elif c.data == +1:
			#capture
			newX = [c.x, c.x + 1]
			newY = [c.y - 1, c.y, c.y + 1]
		elif c.data == -1:
			#capture
			newX = [c.x - 1, c.x]
			newY = [c.y - 1, c.y, c.y + 1]
		for i in newX:
			for j in newY:
				if (i,j) != (x,y):
					if self.turn == +1 and self.board[i][j].data == -1:
						capture.append((i,j))
					elif self.turn == -1 and self.board[i][j].data == +1:
						capture.append((i,j))
		return capture

	def valid_retreats(self,x,y):
		c = self.board[x][y]
		retreat = []
		if c.data == 0:
			return []
		elif c.data == +1:
			#retreat
			newX = [c.x - 2]
			newY = [c.y - 2, c.y, c.y + 2]
		elif c.data == -1:
			#retreat
			newX = [c.x + 2]
			newY = [c.y - 2, c.y, c.y + 2]
		for i in newX:
			for j in newY:
				if (i,j) != (x,y) and self.board[i][j].data == 0:
					retreat.append((i,j))
		return retreat


	def valid_slides(self,p1,p2,p3):
		if p1[0] == p2[0] == p3[0]:
			if p1[0] > 1 or p1[0] < 8:
				return [(p1[0],p1[1]-1),(p1[0],p1[1]+1)]
		elif p1[1] == p2[1] == p3[1]:
			if p1[1] > 1 or p1[1] < 8:
				return [(p1[0]-1,p1[1]),(p3[0]+1,p3[1])]
		elif (p1[0] + p1[1]) == (p2[0] + p2[1]) == (p3[0] + p3[1]):
			return [(p1[0]-1,p1[1]+1),(p3[0]+1),p3[1]-1]
		elif (p3[0]-p2[0]) == (p2[0]-p1[0]) and (p3[1]-p2[1]) == (p2[1]-p1[1]):
			return [(p1[0]-1,p1[1]-1),(p3[0]+1),p3[1]+1]

	def valid_shoot(self,p1,p2,p3):
		if p1[0] == p2[0] == p3[0]:
			if p1[0] > 1 or p1[0] < 8:
				return [(p1[0],p1[1]-2),(p1[0],p1[1]-3),(p1[0],p1[1]+2),(p1[0],p1[1]+3)]
		elif p1[1] == p2[1] == p3[1]:
			if p1[1] > 1 or p1[1] < 8:
				return [(p1[0]-2,p1[1]),(p1[0]-3,p1[1]),(p3[0]+2,p3[1]),(p3[0]+3,p3[1])]
		elif (p1[0] + p1[1]) == (p2[0] + p2[1]) == (p3[0] + p3[1]):
			return [(p1[0]-2,p1[1]+2),(p1[0]-3,p1[1]+3),(p3[0]+2,p3[1]-2),(p3[0]+3,p3[1]-3)]
		elif (p3[0]-p2[0]) == (p2[0]-p1[0]) and (p3[1]-p2[1]) == (p2[1]-p1[1]):
			return [(p1[0]-2,p1[1]-2),(p1[0]-2,p1[1]-3),(p3[0]+2,p3[1]+2),(p3[0]+3,p3[1]+3)]

	def move(self,x,y):
		self.board_backup = copy.deepcopy(self.board)
		moves = self.valid_moves(x,y)
		if len(moves) == 0:
			return False
		else:
			print('moves are:\n')
			print(moves)
			r = int(input('enter move to make '))
			if r > len(moves) or r < 0:
				print('move index out of range')
			else:
				newpos = moves[r]
				self._setcell(Cell(moves[r][0],moves[r][1],data=self.turn))
				self._setcell(Cell(x,y,data=0))
				self._turn_over()
				return True

	def capture(self,x,y):
		self.board_backup = copy.deepcopy(self.board)
		captures = self.valid_captures(x,y)
		if len(captures) == 0:
			return False
		else:
			print('moves are:\n')
			print(captures)
			r = int(input('enter move to make '))
			if r > len(captures) or r < 0:
				print('move index out of range')
			else:
				newpos = captures[r]
				self._setcell(Cell(captures[r][0],captures[r][1],data=self.turn))
				self._setcell(Cell(x,y,data=0))
				self._turn_over()
				return True

	def retreat(self,x,y):
		self.board_backup = copy.deepcopy(self.board)
		retreats = self.valid_retreats(x,y)
		if len(retreats) == 0:
			return False
		else:
			print('moves are:\n')
			print(retreats)
			r = int(input('enter move to make '))
			if r > len(retreats) or x < 0:
				print('move index out of range')
			else:
				newpos = retreats[r]
				self._setcell(Cell(retreats[r][0],retreats[r][1],data=self.turn))
				self._setcell(Cell(x,y,data=0))
				self._turn_over()
				return True

	def slide(self,p1,p2,p3):
		self.board_backup = copy.deepcopy(self.board)
		if not (self.board[p1[0]][p1[1]].data == self.board[p2[0]][p2[1]].data == self.board[p3[0]][p3[1]].data) and (self.board[p3[0]][p3[1]].data == self.turn):
			return False
		slides = self.valid_slides(p1,p2,p3)
		if len(slides) == 0:
			return False
		else:
			print('moves are:\n')
			print(slides)
			r = int(input('enter move to make '))
			if x > len(slides) or x < 0:
				print('move index out of range')
			else:
				newpos = slides[x]
				self._setcell(Cell(slides[x][0],slides[x][1],data=self.turn))
				if x == 0:
					self._setcell(Cell(p3[0],p3[1],data=0))
				elif x == 1:
					self._setcell(Cell(p1[0],p1[1],data=0))
				self._turn_over()
				return True

	def shoot(self,p1,p2,p3):
		self.board_backup = copy.deepcopy(self.board)
		if not (self.board[p1[0]][p1[1]].data == self.board[p2[0]][p2[1]].data == self.board[p3[0]][p3[1]].data) and (self.board[p3[0]][p3[1]].data == self.turn):
			return False
		shots = self.valid_shoot(p1,p2,p3)
		for s in shots:
			if s[0] < 0 or s[0] > 9:
				shots.remove(s)
			elif s[1] < 0 or s[1] > 9:
				shots.remove(s)
		if len(shots) == 0:
			return False
		else:
			print('moves are:\n')
			print(shots)
			r = int(input('enter move to make '))
			if x > len(shots) or x < 0:
				print('move index out of range')
			else:
				newpos = shots[x]
				if self.board[newpos[0]][newpos[1]] == -self.turn:
					self._setcell(Cell(newpos[0],newpos[1],data=self.turn))
				self._turn_over()
				return True

	def gen_move_list(self,x,y):
		m = self.valid_moves(x,y)
		r = self.valid_retreats(x,y)
		c = self.valid_captures(x,y)
		x = m + r + c
		res = list(filter(lambda sub: all(elem >= 0 for elem in sub), x))
		return res


	def __repr__(self):
		retstr = 'turn:{}\nboard:\n'.format(self.turn)
		for i in range(0,10):
			for j in range(0,10):
				retstr += str(self.board[i][j]) + '  '
			retstr += '\n'
		return retstr
