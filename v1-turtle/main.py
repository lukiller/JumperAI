# https://docs.python.org/3/library/turtle.html
# https://realpython.com/python-class-constructor/
# https://www.youtube.com/watch?v=XGf2GcyHPhc&t
# https://www.youtube.com/watch?v=iX_on3VxZzk

import jumper
import random
from ground import Ground
from obstacle import Obstacle
from player import Player
from score import Score
from itertools import filterfalse

distance = 0
gameOver = False

game = jumper.createGame()
Ground.createGround()
scoreboard = Score()
playersManager = Player()
obstacleManager = Obstacle()
character = playersManager.createPlayer()
# tree = obstacleManager.createTree()
# bird = obstacleManager.createBird()
obstacles = []


def jump():
    playersManager.jump(character)


def crouch():
    playersManager.crouch(character)


def standup():
    playersManager.standup(character)


game.listen()
game.onkeypress(jump, "space")
game.onkeyrelease(standup, "Down")
game.onkeypress(crouch, "Down")

next = 50
while True:
    distance += 1
    scoreboard.showScore(distance)
    playersManager.movePlayer(character)

    if distance == next:
        rnd = random.randint(jumper.MIN_DISTANCE, jumper.MAX_DISTANCE)
        next = distance + rnd
        rnd = random.randint(1, 2)
        if rnd == 1:
            obstacle = obstacleManager.createTree()
        else:
            obstacle = obstacleManager.createBird()
        obstacles.append(obstacle)

    for obstacle in obstacles:
        obstacleManager.moveObstacle(obstacle)
        if playersManager.collision(character, obstacle):
            gameOver = True
            character.color("red")

    obstacles[:] = filterfalse(obstacleManager.arrived, obstacles)

    game.update()

    # if gameOver == True:
    #     break
