import turtle
from functools import reduce

arr = [True, False, True, False]
res = all(arr)

arr = [False, False, False, False]
res = all(arr)

arr = [True, True, True, True]
res = all(arr)

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

final = res
