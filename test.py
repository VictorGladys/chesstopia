import code
from gamelogic.board_graph import Board
from gamelogic.player import Player
from gamelogic.pieces import Rook, Bishop, Queen, Knight, King, Pawn
# def main():
# 	Board.build_grid()
# 	while not keyboard.is_pressed('r'):
# 		print_grid()
# 		legal_move(input('move'))
# 	else:
# 		main()
def place_piece(piece, player, board, location ):
	p = piece(player, board, location)
	player.pieces[p.index] = p
	board.pieces[location] = p

def place_pawn(player, board, location, front):
	p = Pawn(player, board, location, front)
	player.pieces[p.index] = p
	board.pieces[location] = p

def main():
	# while True:
	# 	try:
	# 		x = int(input('enter x dimension:'))
	# 		y = int(input('enter y dimension:'))
	# 		break
	# 	except ValueError:
	# 		print('not a number')
	b = Board.square_grid((8, 8))
	p1 = input('player 1 name:')
	p2 = input("player 2 name:")
	p1 = Player(p1, 'green')
	p2 = Player(p2, 'red')
	piecelist = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
	for i in range(8):
		# code.interact(local=dict(globals(), **locals()))
		place_piece(piecelist[i], p1, b, b.name_to_id[(0, i)])
		place_pawn(p1, b, b.name_to_id[(1, i)], [b.name_to_id[(2, i)]])
		place_pawn(p2, b, b.name_to_id[(6, i)], [b.name_to_id[(5, i)]])
		place_piece(piecelist[i], p2, b, b.name_to_id[(7, i)])
	b.print_square()
	# game loop:
	players = {p1:p2, p2:p1}
	current_player = p1
	while True:
		b.print_square()
		# code.interact(local=dict(globals(), **locals()))
		for i in b.pieces.values():
			i.check_options()
		while True:
			inp = input(current_player.color+' move: ')
			try:
				piece = b.pieces[ b.name_to_id[ ( int(inp[0]), int(inp[-1]) ) ] ]
			except KeyError:
				pass
			else:
				if piece.owner == current_player:
					break
				else:
					print('not one of your pieces')

		current_player = players[current_player]
	# p1 = Player(input('player 1 name:'))
	# p2 = Player(input('player 2 name:'))



if __name__ == "__main__":
	main()