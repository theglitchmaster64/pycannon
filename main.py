#!/usr/bin/env python3

from cannon import *

if __name__ == '__main__':
	print('init')
	board = Board()
	p1 = Player('x',board)
	p2 = Player('y',board)
	p1.place_town((0,5))
	p2.place_town((9,4))
	print('board_state\n',board)
