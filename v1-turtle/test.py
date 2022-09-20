import turtle
import numpy as np
import operator
from functools import reduce


matrix = np.zeros((1, 2))
matrix = np.arange(2).reshape(1, 2)
matrix.fill(0)

# --[ player with max distance ]--------------------------------------------------------

players = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]
players[0].distance = 1200
players[1].distance = 1600
players[2].distance = 700
bestPlayer = max(players, key=operator.attrgetter('distance'))
worstPlayer = min(players, key=operator.attrgetter('distance'))

# --[ index of max value ]--------------------------------------------------------
output = np.zeros((1, 3))
output[0][0] = 20
output[0][1] = 45
output[0][2] = 15
# output = [[[20], [45], [15]]]
indexMin = min(range(len(output[0])), key=output[0].__getitem__)
indexMax = max(range(len(output[0])), key=output[0].__getitem__)

# --[ reduce booleans ]--------------------------------------------------------
arr = [True, False, True, False]
res = all(arr)

arr = [False, False, False, False]
res = all(arr)

arr = [True, True, True, True]
res = all(arr)

# --[ reduce objects ]---------------------------------------------------------
players = [turtle.Turtle()]
players[0].gameOver = False
gameOver = reduce(
    lambda result, player: result and player.gameOver, players, True)

players = [turtle.Turtle()]
players[0].gameOver = True
gameOver = reduce(
    lambda result, player: result and player.gameOver, players, True)

players = [turtle.Turtle(), turtle.Turtle()]
players[0].gameOver = True
players[1].gameOver = False
gameOver = reduce(
    lambda result, player: result and player.gameOver, players, True)

players[0].gameOver = True
players[1].gameOver = True
gameOver = reduce(
    lambda result, player: result and player.gameOver, players, True)

players[0].gameOver = False
players[1].gameOver = False
gameOver = reduce(
    lambda result, player: result and player.gameOver, players, True)

# -----------------------------------------------------------------------------
final = res
