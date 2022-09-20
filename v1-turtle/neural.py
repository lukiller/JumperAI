# https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6
# https://github.com/robmarkcole/Useful-python/blob/master/Numpy/Build%20a%20neural%20network.ipynb
# https://towardsdatascience.com/evolving-neural-networks-b24517bb3701
# https://towardsdatascience.com/an-extensible-evolutionary-algorithm-example-in-python-7372c56a557b

import jumper
import numpy as np
import random
from player import Player

# Inputs (3):
#  - next object type
#  - distance to next object
#  - speed
# Outputs (2):
#  - jump
#  - crouch


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


def compute_loss(y_hat, y):
    return ((y_hat - y)**2).sum()


class NeuralNetwork:
    def __init__(self, inputLayerNeurons, hiddenLayerNeurons, outputLayerNeurons):
        self.input = np.zeros(inputLayerNeurons)
        self.weights1 = np.random.rand(inputLayerNeurons, hiddenLayerNeurons)
        self.weights2 = np.random.rand(hiddenLayerNeurons, outputLayerNeurons)

        self.previousOutput = np.zeros((1, outputLayerNeurons))
        self.output = np.zeros((1, outputLayerNeurons))
        # self.previousOutput = np.arange(outputLayerNeurons).reshape(1, outputLayerNeurons)
        # self.output = np.arange(outputLayerNeurons).reshape(1, outputLayerNeurons)
        # self.output = np.zeros(outputLayerNeurons)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))


class NeuralNetwork2:
    def __init__(self, x, hiddenLayerNeurons, y):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1], hiddenLayerNeurons)  # 3 x 4 (3 inputs x 4 hidden)
        self.weights2 = np.random.rand(hiddenLayerNeurons, y.shape[1])  # 4 x 2 -> (4 hidden x 2 outputs)
        self.y = y
        self.output = np.zeros(self.y.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2 * (self.y - self.output) * sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2 * (self.y - self.output) *
                            sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2


def example1():
    hiddenLayerNeurons = 4
    X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])  # 3 inputs, 4 examples
    y = np.array([[0], [1], [0], [1]])  # 1 output, 4 examples
    nn = NeuralNetwork2(X, hiddenLayerNeurons, y)
    loss_values = []
    for i in range(1500):  # me parece que tengo que hacer esto x c/ brain hasta que pierda -> no hasta 1500
        nn.feedforward()
        nn.backprop()
        loss = compute_loss(nn.output, y)
        loss_values.append(loss)
    print(nn.output)
    print(f" final loss : {loss}")


def example2():
    playersManager = Player()
    player = playersManager.createPlayer()
    inputLayerNeurons = 3
    hiddenLayerNeurons = 4
    outputLayerNeurons = 2
    speed = 8
    brain = NeuralNetwork(inputLayerNeurons, hiddenLayerNeurons, outputLayerNeurons)
    obstacleType = 1
    distanceToObstacle = 100
    previousOutput = np.arange(2).reshape(1, 2)
    jumping = 8  # it takes this iterations to land after jumping
    for distance in reversed(range(2000)):
        if player.state == Player.STATE_JUMPING and jumping == 0:
            player.state = Player.STATE_READY
        if (distanceToObstacle == 0):
            distanceToObstacle = random.randint(50, 80)
            obstacleType = 1
            rnd = random.randint(1, 10)
            if rnd > 7:
                obstacleType = 2
        if (distance % 300 == 0):
            speed += 0.1
        brain.input = np.array([[obstacleType, distanceToObstacle, speed]])
        brain.feedforward()
        nextPossibleAction = jumper.calculateNextPlayerAction(previousOutput, brain.output)
        action = playersManager.nextPlayerAction(player, nextPossibleAction)
        # if (distance % 500 == 0):
        print(f"input={brain.input} -> output: {brain.output} | {player.state} | {nextPossibleAction} | {action}")

        if action == jumper.ACTION_STANDUP:
            player.state = Player.STATE_READY
        if action == jumper.ACTION_JUMP:
            player.state = Player.STATE_JUMPING
            jumping = 8
        if action == jumper.ACTION_CROUCH:
            player.state = Player.STATE_CROUCHING
        previousOutput = brain.output
        jumping -= 1
        distance -= 1
        distanceToObstacle -= 1
