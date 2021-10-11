#!/usr/bin/env python3

from player import Player
from game import Game, Cell

if __name__=='__main__':
	g=Game()
	g.move(3,3,4,3)
	g.move(6,2,5,3)
