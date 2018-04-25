import collections
from board_graph import Board 

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

class Piece:
	counter = 0
	def __init__(self, owner, board, location):
		self.owner = owner
		self.board = board
		self.location = location
		self.index = counter
		counter += 1

class Pawn(Piece):
	def __init__(self, owner, board, location, front):
		super(owner, board, location)
		self.front = front
		self.check_options

	def check_options(self):
		self.options = {}
		for j in self.front:
			if j not in self.board.pieces.keys:
				self.options.update({front: 'm'})
			for i in list(self.board.edge_neighbors[j] & self.board.vertex_neighbors[self.location]):
				if (i in self.board.pieces.keys) and (self.board.pieces[i].owner != self.owner):
					self.options.update({i: 'c'})

	def move(self, target):
		self.front = self.board.pass_through[(self.location, target)]
		self.location = target
		self.check_options()

	def capture(self, target):
		fake_history = set(self.board.edge_neighbors[self.location] & (set(self.board.edge_neighbors[self.target]) - set(self.front)))
		self.front = self.board.pass_through[(fake_history, target)]
		self.location = target
		self.board.pieces[target].location = False
		self.board.pieces[target] = self
		del self.board.pieces[location]
		self.check_options()

class Rook(Piece):
	def __init__(self, owner, board, location):
		super(owner, board, location)
		self.check_options()

	def check_options(self):
		frontier = Queue()
		frontier.put(self.location)

		while not frontier.empty():
			current = frontier.get()
			print('visiting %r' % current)
			for next in self.board.pass_through[()]

		for i in self.board.edge_neighbors[self.location]:
			frontier = Queue()
			frontier.put(self.location)
			direction = (self.location, i)
			while i in self.board.name_to_id.keys() and i not in self.board.pieces[self.location]:
				self.options.update({ i : 'm' })
				direction = (direction[1], i)
				i = 
			else:
				if i in self 

def breadth_first_search_1(direction, start):
    # print out what we find
    frontier = Queue()
    frontier.put(start)
    visited = {}
    visited[start] = True
    
    while not frontier.empty():
        current = frontier.get()
        print("Visiting %r" % current)
        for next in direction[current]:
            if next not in visited:
                frontier.put(next)
                visited[next] = True

	return came_from

if __name__ == '__main__':
	b = Board.square_grid((4,4))
	print(b)
	r = Rook(1, b, 1)
	print(r.options)
	p = Pawn(1, b, 1)
	print(p.options)