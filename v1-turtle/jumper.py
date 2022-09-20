import turtle


class Jumper:
    GAME_WIDTH = 800
    GAME_HEIGHT = 350
    TURTLE_SIZE = 20  # This is the default turtle size (20 x 20). The (0, 0) is in the center of the turtle.
    GROUND = -(GAME_HEIGHT / 2 - 50)
    STARTX = GAME_WIDTH / 2
    GRAVITY = -0.8
    SPEED = 8
    START_OBSTACLE_DISTANCE = 50
    MIN_OBSTACLE_DISTANCE = 30
    MAX_OBSTACLE_DISTANCE = 70

    ACTION_NONE = None
    ACTION_JUMP = "jump"
    ACTION_CROUCH = "crouch"
    ACTION_STANDUP = "standup"

    NN_INPUT_LAYER_SIZE = 3
    NN_HIDDEN_LAYER_SIZE = 4
    NN_OUTPUT_LAYER_SIZE = 2

    MAX_PLAYERS = 100
    MAX_GENERATIONS = 3

    Colors = ["dodgerblue", "maroon", "navy", "indianred", "goldenrod",
              "forestgreen", "darkorange", "turquoise", "olive", "darkviolet"]

    ground = turtle.Turtle()
    status = turtle.Turtle()

    def createGame(self):
        game = turtle.Screen()
        game.title("Jumper AI")
        game.bgcolor("black")
        game.setup(width=Jumper.GAME_WIDTH, height=Jumper.GAME_HEIGHT)
        game.tracer(0)
        self.createGround()
        self.createStatus()
        return game

    def createGround(self):
        self.ground.speed(0)
        self.ground.pensize(3)
        self.ground.shape("square")
        self.ground.color("brown")
        self.ground.penup()
        self.ground.goto(-Jumper.STARTX, Jumper.GROUND)
        self.ground.pendown()
        self.ground.goto(Jumper.STARTX, Jumper.GROUND)
        self.ground.penup()

    def createStatus(self):
        self.status.speed(0)
        self.status.shape("square")
        self.status.color("gray")
        self.status.penup()
        self.status.hideturtle()
        self.status.goto(-(Jumper.GAME_WIDTH / 2) + 50, -(Jumper.GAME_HEIGHT / 2) + 20)
        self.status.write("---")

    def showStatus(self, text):
        self.status.clear()
        self.status.write(text, font=("Courier", 16, "normal"))

    def calculateNextPlayerAction(self, previousOutput, currentOutput):
        jump = 0
        crouch = 1
        if previousOutput[0][jump] == currentOutput[0][jump] and previousOutput[0][crouch] == currentOutput[0][crouch]:
            return None
        if previousOutput[0][jump] != currentOutput[0][jump] and previousOutput[0][crouch] != currentOutput[0][crouch]:
            action = max(range(len(currentOutput[0])), key=currentOutput[0].__getitem__)
            if (action == jump):
                return Jumper.ACTION_JUMP
            return Jumper.ACTION_CROUCH
        if previousOutput[0][jump] != currentOutput[0][jump]:
            return Jumper.ACTION_JUMP
        return Jumper.ACTION_CROUCH
