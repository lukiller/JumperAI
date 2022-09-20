# https://docs.python.org/3/library/turtle.html
# https://realpython.com/python-class-constructor/
# https://www.youtube.com/watch?v=XGf2GcyHPhc&t
# https://www.youtube.com/watch?v=iX_on3VxZzk

from functools import reduce
from jumper import Jumper
import random
import operator
from obstacle import Obstacle
from player import Player
from score import Score
from itertools import filterfalse
from neural import NeuralNetwork
import numpy as np


jumper = Jumper()
playerIsHuman = True


def initPlayers():
    players = []
    maxColors = len(jumper.Colors)
    for p in range(jumper.MAX_PLAYERS):
        player = playersManager.createPlayer(jumper.Colors[p % maxColors])
        player.brain = NeuralNetwork(jumper.NN_INPUT_LAYER_SIZE,
                                     jumper.NN_HIDDEN_LAYER_SIZE,
                                     jumper.NN_OUTPUT_LAYER_SIZE)
        # if parent != None:
        #     player.brain.weights1 = np.copy(parent.brain.weights1)
        #     player.brain.weights2 = np.copy(parent.brain.weights2)
        players.append(player)
    return players


def resetPlayers(players, parent):
    for player in players:
        playersManager.resetPlayer(player)
        if parent != None:
            player.brain.weights1 = np.copy(parent.brain.weights1)
            player.brain.weights2 = np.copy(parent.brain.weights2)


def jump():
    for player in filter(lambda player: not player.gameOver, players):
        player.action = jumper.ACTION_JUMP
        playersManager.jump(player)


def crouch():
    for player in filter(lambda player: not player.gameOver, players):
        player.action = jumper.ACTION_CROUCH
        playersManager.crouch(player)


def standup():
    for player in filter(lambda player: not player.gameOver, players):
        player.action = jumper.ACTION_STANDUP
        playersManager.standup(player)


# TEST --------------------------------------------------------------------
def jump1():
    players[0].action = jumper.ACTION_JUMP
    playersManager.jump(players[0])


def jump2():
    players[1].action = jumper.ACTION_JUMP
    playersManager.jump(players[1])


def crouch1():
    players[0].action = jumper.ACTION_CROUCH
    playersManager.crouch(players[0])


def crouch2():
    players[1].action = jumper.ACTION_CROUCH
    playersManager.crouch(players[1])


def standup1():
    players[0].action = jumper.ACTION_STANDUP
    playersManager.standup(players[0])


def standup2():
    players[1].action = jumper.ACTION_STANDUP
    playersManager.standup(players[1])
# TEST --------------------------------------------------------------------


def movePlayers(players, obstacles, distance):
    for player in filter(lambda player: not player.gameOver, players):
        player.distance = distance
        movePlayer(player, obstacles)


def movePlayer(player, obstacles):
    if len(obstacles) == 0 or player.gameOver:
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


def thinkNextActions(players, obstacles):
    for player in players:
        if len(obstacles) == 0 or player.gameOver or not hasattr(player, 'nextObstacleType'):
            continue
        player.brain.input = np.array([[player.nextObstacleType, player.distanceToNextObstacle, jumper.SPEED]])
        player.brain.feedforward()
        nextPossibleAction = jumper.calculateNextPlayerAction(player.brain.previousOutput, player.brain.output)
        player.brain.previousOutput = player.brain.output
        action = playersManager.nextPlayerAction(player, nextPossibleAction)
        if action != jumper.ACTION_NONE:
            player.action = action
        if action == jumper.ACTION_JUMP:
            playersManager.jump(player)
        if action == jumper.ACTION_CROUCH:
            playersManager.crouch(player)
        if action == jumper.ACTION_STANDUP:
            playersManager.standup(player)


def listenKeys():
    game.listen()
    game.onkeypress(jump, "space")
    game.onkeyrelease(standup, "Down")
    game.onkeypress(crouch, "Down")
    # TEST
    game.onkeypress(jump1, "1")
    game.onkeypress(jump2, "2")
    game.onkeyrelease(standup1, "9")
    game.onkeyrelease(standup2, "0")
    game.onkeypress(crouch1, "9")
    game.onkeypress(crouch2, "0")


def unlistenKeys():
    game.onkeypress(None, "space")
    game.onkeyrelease(None, "Down")
    game.onkeypress(None, "Down")


# --[ Main program ]-----------------------------------------
game = jumper.createGame()
scoreboard = Score()
playersManager = Player()
obstacleManager = Obstacle()

generations = jumper.MAX_GENERATIONS
if playerIsHuman:
    generations = 1
    listenKeys()

players = initPlayers()
bestPlayer = None
obstacles = []
# obstaclesDispose = []
generation = 1
while generation <= generations:
    resetPlayers(players, bestPlayer)
    # disposear todo
    # for obs in obstacles:
    #     obs.reset()
    # for pl in players:
    #     pl.reset()
    # game.update()

    # initPlayers(bestPlayer)
    distance = 0
    obstacles.clear()
    nextObstacleDistance = jumper.START_OBSTACLE_DISTANCE
    gameOver = False
    while not gameOver:
        game.tracer(0, 0)
        distance += 1
        if playerIsHuman:
            scoreboard.showScore(distance)
        else:
            scoreboard.showScore(distance, generation)
        movePlayers(players, obstacles, distance)

        if distance == nextObstacleDistance:
            nextObstacleDistance = createNextObstacle(distance, obstacles)

        moveObstacles(obstacles, players)

        # obstaclesDispose = filter(obstacleManager.arrived, obstacles)
        obstacles[:] = filterfalse(obstacleManager.arrived, obstacles)
        gameOver = reduce(lambda result, player: result and player.gameOver, players, True)

        if not playerIsHuman:
            thinkNextActions(players, obstacles)

        # disposear todo
        # for obs in obstaclesDispose:
        #     obs.reset()

        game.update()

    if playerIsHuman:
        scoreboard.showFinish(distance)
    else:
        scoreboard.showFinish(distance, generation)
        bestPlayer = max(players, key=operator.attrgetter('distance'))
        game.delay(2000)
        game = jumper.createGame()
        scoreboard = Score()
        playersManager = Player()
        obstacleManager = Obstacle()

    generation += 1

if playerIsHuman:
    unlistenKeys()

# Prevent game from auto-closing
while True:
    game.update()
