# https://docs.python.org/3/library/turtle.html
# https://realpython.com/python-class-constructor/
# https://www.youtube.com/watch?v=XGf2GcyHPhc&t
# https://www.youtube.com/watch?v=iX_on3VxZzk

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
    for player in filter(lambda player: not player.gameOver, players):
        player.action = jumper.ACTION_JUMP
        playersManager.jump(player)


def jump1():
    players[0].action = jumper.ACTION_JUMP
    playersManager.jump(players[0])


def jump2():
    players[1].action = jumper.ACTION_JUMP
    playersManager.jump(players[1])


def crouch():
    for player in filter(lambda player: not player.gameOver, players):
        player.action = jumper.ACTION_CROUCH
        playersManager.crouch(player)


def standup():
    for player in filter(lambda player: not player.gameOver, players):
        player.action = jumper.ACTION_STANDUP
        playersManager.standup(player)


def movePlayers(players, obstacles, distance):
    for player in filter(lambda player: not player.gameOver, players):
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
    game.onkeypress(jump1, "1")
    game.onkeypress(jump2, "2")


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
    gameOver = reduce(lambda result, player: result and player.gameOver, players, True)

    for player in players:
        # pasar cada player a la AI
        # la AI va a decir que tecla presionar
        # ver donde poner esto, si acá o más arriba
        pass

    game.update()

unlistenKeys()
scoreboard.showFinish(distance)

# Prevent game from auto-closing
while True:
    game.update()
