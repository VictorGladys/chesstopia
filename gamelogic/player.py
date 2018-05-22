class Player():
	counter = 0
	def __init__(self, alias, color):
		self.index = Player.counter
		Player.counter += 1
		self.pieces = {}
		self.score = 0
		self.alias = alias
		self.color = color