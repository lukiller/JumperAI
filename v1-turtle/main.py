# https://docs.python.org/3/library/turtle.html
# https://realpython.com/python-class-constructor/
# https://www.youtube.com/watch?v=XGf2GcyHPhc&t
# https://www.youtube.com/watch?v=iX_on3VxZzk

# In order to make AI exeute actions along all the players
# every action is set to the player and then executed by
# the player manager

from functools import reduce
import jumper
import random
from ground import Ground
from obstacle import Obstacle
from player import Player
from score import Score
from itertools import filterfalse

distance = 0
gameOver = False
automatic = False  # Execute actions in automatic mode (for AI)

game = jumper.createGame()
Ground.createGround()
scoreboard = Score()
playersManager = Player()
obstacleManager = Obstacle()
obstacles = []
players = []
maxColors = len(jumper.Colors)
for p in range(jumper.MAX_PLAYERS):
    players.append(playersManager.createPlayer(
        p, jumper.Colors[p % maxColors]))


def jump():
    for player in players:
        player.action = jumper.ACTION_JUMP
        if not automatic:
            playersManager.jump(player)


def crouch():
    for player in players:
        player.action = jumper.ACTION_CROUCH
        if not automatic:
            playersManager.crouch(player)


def standup():
    for player in players:
        player.action = jumper.ACTION_STANDUP
        if not automatic:
            playersManager.standup(player)


def movePlayers(players, obstacles, distance):
    for player in players:
        player.distance = distance
        movePlayer(player, obstacles)


def movePlayer(player, obstacles):
    if len(obstacles) == 0:
        return
    type = obstacles[0].type
    distanceToNextObstacle = (obstacles[0].xcor() - obstacles[0].width / 2) - (player.xcor() + player.width / 2)
    if distanceToNextObstacle <= 0:  # assumes there is always more than 1 obstacle
        type = obstacles[1].type
        distanceToNextObstacle = (obstacles[1].xcor() - obstacles[1].width / 2) - (player.xcor() + player.width / 2)
    player.nextObstacleType = type
    player.distanceToNextObstacle = distanceToNextObstacle
    playersManager.movePlayer(player)


def createNextObstacle(distance, obstacles):
    rnd = random.randint(jumper.MIN_OBSTACLE_DISTANCE,
                         jumper.MAX_OBSTACLE_DISTANCE)
    next = distance + rnd
    rnd = random.randint(1, 2)
    if rnd == 1:
        obstacle = obstacleManager.createTree()
    else:
        obstacle = obstacleManager.createBird()
    obstacles.append(obstacle)
    return next


def moveObstacles(obstacles, players):
    for obstacle in obstacles:
        moveObstacle(obstacle, players)


def moveObstacle(obstacle, players):
    obstacleManager.moveObstacle(obstacle)
    for player in players:
        if playersManager.collision(player, obstacle):
            player.gameOver = True
            player.color("red")


def listenKeys():
    game.listen()
    game.onkeypress(jump, "space")
    game.onkeyrelease(standup, "Down")
    game.onkeypress(crouch, "Down")


def unlistenKeys():
    game.onkeypress(None, "space")
    game.onkeyrelease(None, "Down")
    game.onkeypress(None, "Down")


listenKeys()
next = jumper.START_OBSTACLE_DISTANCE
while not gameOver:
    game.tracer(0, 0)
    distance += 1
    scoreboard.showScore(distance)
    movePlayers(players, obstacles, distance)

    if distance == next:
        next = createNextObstacle(distance, obstacles)

    moveObstacles(obstacles, players)
    obstacles[:] = filterfalse(obstacleManager.arrived, obstacles)
    gameOver = reduce(
        lambda result, player: result and player.gameOver, players, True)

    game.update()

unlistenKeys()
scoreboard.showFinish(distance)

# Prevent game from auto-closing
while True:
    game.update()
