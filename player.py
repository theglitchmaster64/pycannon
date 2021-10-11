class Player:
	def __init__(self,color):
		self.type = color

	def __repr__(self):
		retstr = 'player:{0}'.format(self.type)
		return retstr
