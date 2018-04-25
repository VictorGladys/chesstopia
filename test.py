import keyboard
from gamelogic.board_graph import Board

def main():
	Board.build_grid()
	while not keyboard.is_pressed('r'):
		print_grid()
		legal_move(input('move'))
	else:
		main()




if __name__ == "__test__":
	main()