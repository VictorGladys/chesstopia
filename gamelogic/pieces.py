import collections
# from board_graph import Board
# from player import player
import code 
# code.interact(local=dict(globals(), **locals()))

class Queue:
	# queue class for pathfinding
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()
class LocationError(Exception):
	pass

class Piece:
	# base class for game pieces: 
	# owner: player instance, contains player pieces and drawing colors
	# board: board instance, contains node relations pieces on board
	# location: id of node it is currently on (nill means not on board)
	# id: auto updates index counter
	counter = 0
	def __init__(self, owner, board, location):
		self.owner = owner
		self.board = board
		if location in self.board.pieces.keys():
			raise LocationError('There is already a piece there')
		self.location = location
		if location != None:
			self.board.pieces[self.location] = self
		self.index = Piece.counter
		Piece.counter += 1

	def straight_ahead(self, start_directions, owner):
		# follows straight (possibly splitting) line till it hits borders or pieces
		frontier = Queue()
		for i in start_directions: frontier.put(i)
		while not frontier.empty():
			current = frontier.get()
			if self.board.pass_through.get(current) != None:
				for i in self.board.pass_through.get(current):
					next = (current[1], i)
					if self.board.legal(i, self.owner):
						if i in self.board.pieces.keys():
							self.options.update({ i: 'c' })  
						else:
							self.options.update({ i: 'm' })
							frontier.put((current[1], i))

	def move(self, target):
		# moving goes in 2 steps, capturing in 3:
		# 1: delete piece from where it came:
		# 2: update location and lists it appears in (only piece listing atm, except for en_passant)
		# 3: if a piece was captured, remove from the board + additional rules (shogi/crazyhouse)
		try: 
			move = self.options[target]
		except KeyError: 
			print('not a valid move')
		else:
			if move == 'c':
				self.board.pieces[target].location = None
			del self.board.pieces[self.location]
			self.board.pieces[target] = self
			self.location = target


class Pawn(Piece):
	# pawns have a facing, translated in which square(s) is(are) in front of it
	def __init__(self, owner, board, location, front):
		super().__init__(owner, board, location)
		self.front = front
		self.check_options
		self.alias = 'p'
		self.first_step = True

	def check_options(self):
	# moving: all fronts are checked
	# capturing: neighbours edge to front and vertex to currentlocation are checked for pieces and en_passant ghosts
		self.options = {}
		for j in self.front:
			if j not in self.board.pieces.keys():
				self.options.update({ j: 'm'})
			for i in list(set(self.board.edge_neighbors[j]) & set(self.board.vertex_neighbors[self.location])):
				if (i in self.board.pieces.keys()) and (self.board.pieces[i].owner != self.owner):
					self.options.update({i: 'c'})
				elif (i in self.board.en_passant.keys() and self.board.en_passant[i].owner != self.owner):
					self.options.update({i: 'e'})			
		
		if self.first_step:
			self.two_step()

	def two_step(self):
		# first move can be double, ghost is saved in en_passant list for 1 turn
		for i in self.front:
			if self.board.empty(i): 
				for j in self.board.pass_through[( self.location, i )]:
					if self.board.empty(j): 
						self.options.update({ j: 'd' })

	def move(self, target):
		# pawns are weird:
		# 1: delete piece from board
		# 2&3: dependent on type of move
		try: move_type = self.options[target]
		except IndexError: print('not a valid move')
		else:
			del self.board.pieces[self.location]
			if move_type == 'm':
				step(target)
			elif move_type == 'c':
				capture(target)
			elif move_type == 'd':
				double_step(target)
			elif move_type == 'e':
				en_passant(target)
			self.board.pieces[self.location] = self
		self.check_options()

	def en_passant(self, target):
		# 2: update location and decide new front (target piece reverse pass_through)
		# 3: delete target from board
		en_passant_target = self.en_passant[target]
		self.location = target
		self.front = self.board.pass_through[(en_passant_target.location, target)]
		del self.board.pieces[en_passant_target.location]

	def step(self, target):
		# 2: update location and front
		self.front = self.board.pass_through[(self.location, target)]
		self.location = target

	def double_step(self,target):
		# 2: update location and front based on pass_through from 
		self.front = self.board.pass_through[(self.front, target)]
		self.location = target
		self.board.en_passant.update({ target: self })

	def capture(self, target):
		fake_history = set(self.board.edge_neighbors[self.location] & (set(self.board.edge_neighbors[self.target]) - set(self.front)))
		self.front = self.board.pass_through[(fake_history, target)]
		self.location = target
		self.board.pieces[target].location = False
		del self.board.pieces[location]

class Rook(Piece):
	def __init__(self, owner, board, location):
		super().__init__(owner, board, location)
		self.alias = 'r'

	# all edge neighbors, straight ahead
	def check_options(self):
		self.options = {}
		start_directions = []
		for i in self.board.edge_neighbors[self.location]:
			if self.board.legal(i, self.owner):
				if i in self.board.pieces.keys():
							self.options.update({ i: 'c' })
				else: 
					start_directions.append((self.location, i))
					self.options.update({ i: 'm' })
				# print('visiting %r' % current)
		if len(start_directions) != 0: self.straight_ahead(start_directions, self.owner)

class Bishop(Piece):
	def __init__(self, owner, board, location):
		super().__init__(owner, board, location)
		self.alias = 'b'
		self.options = {}

	# all vertex neigbours, straight ahead
	def check_options(self):
		start_directions = []
		for i in self.board.vertex_neighbors[self.location]:
			if self.board.legal(i, self.owner):
				if i in self.board.pieces.keys():
							self.options.update({ i: 'c' })
				else: 
					start_directions.append((self.location, i))
					self.options.update({ i: 'm' })
				# print('visiting %r' % current)
		if len(start_directions) != 0: self.straight_ahead(start_directions, self.owner)

class Queen(Piece):
	def __init__(self, owner, board, location):
		super().__init__(owner, board, location)
		self.alias = 'q'

	# all neighbors, straight ahead 
	def check_options(self):
		self.options = {}
		start_directions = []
		for i in (self.board.vertex_neighbors[self.location] + self.board.edge_neighbors[self.location]):
			if self.board.legal(i, self.owner):
				if i in self.board.pieces.keys():
							self.options.update({ i: 'c' })
				else: 
					start_directions.append((self.location, i))
					self.options.update({ i: 'm' })
				# print('visiting %r' % current)
		if len(start_directions) != 0: self.straight_ahead(start_directions, self.owner)

class Knight(Piece):
	def __init__(self, owner, board, location):
		super().__init__(owner, board, location)
		self.alias = 'k'
	# knight movement is done both ways to allow for around the corner maneuvres on exotic maps
	def check_options(self): 
		self.options = {}
		self.long_short()
		self.short_long()
		self.alias = 'k'

	# first pass through egde neighbors. 
	# then take intersection of edge neighbors of second node and vertex neighbors of first node to make a turn
	def long_short(self):
		two_away = []
		for edge_neighbor in self.board.edge_neighbors[self.location]:
			try: options = self.board.pass_through[(self.location, edge_neighbor)]
			except KeyError:
				pass
			else:
				for i in options:
					two_away.append(i)
		if len(two_away) == 0:
			return
		# two_away = [ self.board.pass_through[(self.location, edge_neighbor)] for edge_neighbor in self.board.edge_neighbors[self.location] ]
		try: two_away_edge_neighbors = [ self.board.edge_neighbors[option] for option in two_away ]
		except TypeError:
			code.interact(local=dict(globals(), **locals()))
		one_away_vertex_neighbors = [ self.board.vertex_neighbors[edge_neighbor] for edge_neighbor in self.board.edge_neighbors[self.location] ]
		possible_options = [ i for i in two_away_edge_neighbors if i in one_away_vertex_neighbors ]
		for i in possible_options:
			if self.board.legal(i, self.owner):
				if i in self.board.pieces.keys(): self.options.update({ i: 'c' })
				else: self.options.update({ i: 'm' })

	# start at edge neighbors, then walk through vertex neighbors 
	def short_long(self):
		for i in self.board.edge_neighbors[self.location]:
			for j in self.board.vertex_neighbors[self.location]:
				destinations = self.board.pass_through.get((i, j))
				if destinations:
					for destination in destinations: 
						if self.legal(destination, self.owner):
							if destination in self.board.pieces.keys(): self.options.update({ destination: 'c' })
							else: self.options.update({ destination: 'm' })

class King(Piece):
	def __init__(self, owner, board, location):
		super().__init__(owner, board, location)
		self.alias = 'K'

	def check_options(self):
		for i in (self.board.edge_neighbors[self.location] + self.board.vertex_neighbors[self.location]):
			pass

if __name__ == '__main__':
	b = Board.square_grid((4,4))
	print(b)
	r = Rook(1, b, 1)
	r2 = Rook(0, b, 2)
	code.interact(local=dict(globals(), **locals()))
	r.check_options()
	print(r.options)
	# p = Pawn(1, b, 1)
	# print(p.options)