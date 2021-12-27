import numpy

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
		self.board_backup = numpy.empty((10,10), dtype=object)
		self.metadata = ''
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

	def snapshot(self):
		self.board_backup = numpy.copy(self.board)

	def restore(self):
		self.board = numpy.copy(self.board_backup)
		self._turn_over()

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
		if xp == 0:
			score += 1000
		elif yp == 0:
			score -= 1000
		return score

	def is_game_over(self):
		score = self.eval_board()
		if score >= 777 or score <= -777:
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
		try:
			for i in newX:
				for j in newY:
					if (i,j) != (x,y) and self.board[i][j].data == 0:
						move.append((i,j))
		except IndexError as e:
			pass
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
		try:
			for i in newX:
				for j in newY:
					if (i,j) != (x,y):
						if self.turn * self.board[i][j].data == -1:
							capture.append((i,j))
		except IndexError as e:
			pass
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
		try:
			for i in newX:
				for j in newY:
					if (i,j) != (x,y) and self.board[i][j].data == 0:
						retreat.append((i,j))
		except IndexError as e:
			pass
		return retreat

	def valid_shoot(self,x,y):
		try:
			c = self.board[x][y]
			retlist = []
			if c.data == 0:
				return []
			else:
				if self.board[x][y].data == self.board[x-1][y].data == self.board[x+1][y].data:
					retlist = [(x-4,y),(x-3,y),(x+3,y),(x+4,y)]
				elif self.board[x][y].data == self.board[x][y+1].data == self.board[x][y-1].data:
					retlist = [(x,y-4),(x,y-3),(x,y+3),(x,y+4)]
				elif self.board[x][y].data == self.board[x-1][y-1].data == self.board[x+1][y+1].data:
					retlist = [(x-4,y-4),(x-3,y-3),(x+3,y+3),(x+4,y+4)]
				elif self.board[x][y].data == self.board[x-1][y+1].data == self.board[x+1][y-1].data:
					retlist = [(x+4,y-4),(x+3,y-3),(x-3,y+3),(x-4,y+4)]
				else:
					self.metadata = ''
				retlist = list(filter(lambda sub: all(elem >= 0 for elem in sub), retlist))
		except IndexError as e:
			pass
		return retlist

	def valid_slides(self,x,y):
		try:
			c = self.board[x][y]
			retlist = []
			if c.data == 0:
				return []
			else:
				if self.board[x][y].data == self.board[x-1][y].data == self.board[x+1][y].data:
					retlist = [(x-2,y),(x-1,y),(x,y),(x+1,y),(x+2,y)]
				elif self.board[x][y].data == self.board[x][y+1].data == self.board[x][y-1].data:
					retlist = [(x,y-2),(x,y-1),(x,y),(x,y+1),(x,y+2)]
				elif self.board[x][y].data == self.board[x-1][y-1].data == self.board[x+1][y+1].data:
					retlist = [(x+2,y+2),(x-1,y-1),(x,y),(x+1,y+1),(x-2,y-2)]
				elif self.board[x][y].data == self.board[x-1][y+1].data == self.board[x+1][y-1].data:
					retlist = [(x-1,y+2),(x-1,y+1),(x,y),(x+1,y-1),(x+2,y-2)]
				else:
					self.metadata = ''
				retlist = list(filter(lambda sub: all(elem >= 0 for elem in sub), retlist))
		except IndexError as e:
			pass
		return retlist


	def gen_move_list(self,x,y):
		m = self.valid_moves(x,y)
		r = self.valid_retreats(x,y)
		c = self.valid_captures(x,y)
		res_m = list(filter(lambda sub: all(elem >= 0 for elem in sub), m))
		res_r = list(filter(lambda sub: all(elem >= 0 for elem in sub), r))
		res_c = list(filter(lambda sub: all(elem >= 0 for elem in sub), c))
		res_sl = self.valid_slides(x,y)
		res_sh = self.valid_shoot(x,y)
		return {'pos':(x,y),'moves':res_m,'retreats':res_r,'captures':res_c,'slides':res_sl,'shoot':res_sh}


	def move(self,x,y,pos):
		self.snapshot()
		moves = self.gen_move_list(x,y)['moves']
		if len(moves) == 0:
			return False
		if pos not in moves:
			return False
		else:
			self._setcell(Cell(x,y,data=0))
			self._setcell(Cell(pos[0],pos[1],data=self.turn))
			self._turn_over()
			return True

	def capture(self,x,y,pos):
		self.snapshot()
		captures = self.gen_move_list(x,y)['captures']
		if len(captures) == 0:
			return False
		if pos not in captures or self.board[pos[0]][pos[1]].data == 0 or self.board[pos[0]][pos[1]]:
			return False
		else:
			self._setcell(Cell(x,y,data=0))
			self._setcell(Cell(pos[0],pos[1],data=self.turn))
			self._turn_over()
			return True

	def retreat(self,x,y,pos):
		self.snapshot()
		retreats = self.gen_move_list(x,y)['retreats']
		if len(retreats) == 0:
			return False
		if pos in retreats or self.board[pos[0]][pos[1]].data == 0:
			self._setcell(Cell(x,y,data=0))
			self._setcell(Cell(pos[0],pos[1],data=self.turn))
			self._turn_over()
			return True

	def slide(self,x,y,flag=1):
		try:
			self.snapshot()
			slides = self.gen_move_list(x,y)['slides']
			if len(slides) == 0:
				return False
			if flag == -1:
				pos = slides[0]
			else:
				pos = slides[-1]
			if pos in slides and self.board[pos[0]][pos[1]].data == 0:
				if flag == -1:
					for t in range(0,3):
						self._setcell(Cell(slides[t][0],slides[t][1],data=self.turn))
					for s in range(3,5):
						self._setcell(Cell(slides[s][0],slides[s][1],data=0))
				elif flag == 1:
					for t in range(0,2):
						self._setcell(Cell(slides[t][0],slides[t][1],data=0))
					for s in range(2,5):
						self._setcell(Cell(slides[s][0],slides[s][1],data=self.turn))
				self._turn_over()
		except Exception as e:
			pass
		return True

	def shoot(self,x,y,pos):
		try:
			self.snapshot()
			shoots = self.gen_move_list(x,y)['shoot']
			if len(shoots) == 0:
				return False
			if pos not in shoots or self.board[pos[0]][pos[1]].data != -self.turn:
				return False
			else:
				self._setcell(Cell(pos[0],pos[1],data=0))
				self._turn_over()
				return True
		except:
			pass

	def __repr__(self):
		retstr = 'turn:{}\nboard:\n'.format(self.turn)
		for i in range(0,10):
			for j in range(0,10):
				retstr += str(self.board[i][j]) + '  '
			retstr += '\n'
		return retstr
