class Player:
	def __init__(self,type):
		self.type = type
		self.pieces = []

	def get_pieces(self,game):
		for i in range(0,10):
			for j in range(0,10):
				if game.board[i][j].data == self.type:
					self.pieces.append(game.board[i][j])

	def __repr__(self):
		retstr = 'player:{0}\n{1}\n'.format(self.type,self.pieces)
		return retstr

	def __len__(self):
		return len(self.pieces)
