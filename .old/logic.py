
INF = 99999

def minmax(game,player,depth,alpha,beta):
	score = game.eval_board()
	if score > 777 or score < -777:
		return score
	if game.is_game_over():
		return score
	if player == 1:
		best = -INF
		for i in range(0,10):
			for j in range(0,10):
				if game.board[i][j].data == player:
					table = game.gen_move_list(i,j)
					for pos in table['moves']:
						game.move(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						alpha = max(best,alpha)
						if beta <= alpha:
							break
						game.restore()
					for pos in table['captures']:
						game.capture(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						alpha = max(best,alpha)
						if beta <= alpha:
							break
						game.restore()
					for pos in table['retreats']:
						game.retreat(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						alpha = max(best,alpha)
						if beta <= alpha:
							break
						game.restore()
					for pos in table['slides']:
						for x in [-1,1]:
							game.slide(i,j,x)
							best = max(best,minmax(game,-player,depth+1,alpha,beta))
							alpha = max(best,alpha)
							if beta <= alpha:
								break
							game.restore()
					for pos in table['shoot']:
						game.shoot(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						alpha = max(best,alpha)
						if beta <= alpha:
							break
						game.restore()
	elif player == -1:
		best = INF
		for i in range(0,10):
			for j in range(0,10):
				if game.board[i][j].data == player:
					table = game.gen_move_list(i,j)
					for pos in table['moves']:
						game.move(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						beta = min(best,beta)
						if beta <= alpha:
							break
						game.restore()
					for pos in table['captures']:
						game.capture(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						beta = min(best,beta)
						if beta <= alpha:
							break
						game.restore()
					for pos in table['retreats']:
						game.retreat(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						beta = min(best,beta)
						if beta <= alpha:
							break
						game.restore()
					for pos in table['slides']:
						for x in [-1,1]:
							game.slide(i,j,x)
							best = max(best,minmax(game,-player,depth+1,alpha,beta))
							beta = min(best,beta)
							if beta <= alpha:
								break
							game.restore()
					for pos in table['shoot']:
						game.shoot(i,j,pos)
						best = max(best,minmax(game,-player,depth+1,alpha,beta))
						beta = min(best,beta)
						if beta <= alpha:
							break
						game.restore()
	return best
