import turtle
from jumper import Jumper


class Obstacle:
    OBSTACLE_TREE = 1
    OBSTACLE_BIRD = 2

    TREE_WIDTH = 1
    TREE_HEIGHT = 5
    TREE_GROUND = Jumper.GROUND + ((TREE_HEIGHT * Jumper.TURTLE_SIZE) / 2)

    BIRD_WIDTH = 2
    BIRD_HEIGHT = 4
    BIRD_GROUND = 50 + Jumper.GROUND + ((BIRD_HEIGHT * Jumper.TURTLE_SIZE) / 2)

    def createTree(self):
        tree = turtle.Turtle()
        tree.type = Obstacle.OBSTACLE_TREE
        tree.speed(0)
        tree.shape("square")
        tree.shapesize(stretch_wid=Obstacle.TREE_HEIGHT, stretch_len=Obstacle.TREE_WIDTH)
        tree.width = Obstacle.TREE_WIDTH * Jumper.TURTLE_SIZE
        tree.height = Obstacle.TREE_HEIGHT * Jumper.TURTLE_SIZE
        tree.color("green")
        tree.dx = 0
        tree.penup()
        tree.inix = Jumper.GAME_WIDTH / 2 + (Obstacle.TREE_WIDTH * Jumper.TURTLE_SIZE) / 2
        tree.iniy = Obstacle.TREE_GROUND
        tree.goto(tree.inix, tree.iniy)
        tree.arrived = False
        return tree

    def createBird(self):
        bird = turtle.Turtle()
        bird.type = Obstacle.OBSTACLE_BIRD
        bird.speed(0)
        bird.shape("square")
        bird.shapesize(stretch_wid=Obstacle.BIRD_HEIGHT,
                       stretch_len=Obstacle.BIRD_WIDTH)
        bird.width = Obstacle.BIRD_WIDTH * Jumper.TURTLE_SIZE
        bird.height = Obstacle.BIRD_HEIGHT * Jumper.TURTLE_SIZE
        bird.color("yellow")
        bird.dx = 0
        bird.penup()
        bird.inix = Jumper.GAME_WIDTH / 2 + (Obstacle.BIRD_WIDTH * Jumper.TURTLE_SIZE) / 2
        bird.iniy = Obstacle.BIRD_GROUND
        bird.goto(bird.inix, bird.iniy)
        bird.arrived = False
        return bird

    def moveObstacle(self, obstacle):
        obstacle.setx(obstacle.xcor() - Jumper.SPEED)

    def arrived(self, obstacle):
        if obstacle.xcor() <= -(Jumper.GAME_WIDTH / 2) - obstacle.width:
            return True
        return False

    def reset(self, obstacle):
        obstacle.goto(obstacle.inix, obstacle.iniy)
