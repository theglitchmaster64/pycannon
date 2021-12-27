#!/usr/bin/env python3

import sys
sys.setrecursionlimit(1500)

from player import Player
from game import Game, Cell
from logic import minmax

if __name__=='__main__':
	g=Game()
	px = Player('X')
	py = Player('Y')
	print('welcome to pycannon')
	print('''commands:
			g.move -> move
			g.capture -> capture
			g.retreat -> retreat
			g.slide -> slide
			g.shoot -> shoot
			g.restore() -> undo to previous turn
			g._turn_ovre -> end turn (implicit)
			g.is_game_over() -> check for endstate
			g.eval_board -> evaluation function to create a score
			minmax() -> minmax with alpha and beta pruning

			use g to show the board

			1 represents player X (Human)
			-1 represents player Y (CPU)
			0 represents an empty space
			X and Y represent the towns respectively

	''')
	print(g)
