import turtle

GAME_WIDTH = 800
GAME_HEIGHT = 350
TURTLE_SIZE = 20  # This is the default turtle size (20 x 20)
GROUND = -(GAME_HEIGHT / 2 - 50)
STARTX = GAME_WIDTH / 2
GRAVITY = -0.8
SPEED = 8
MIN_DISTANCE = 30
MAX_DISTANCE = 70

status = turtle.Turtle()


def createGame():
    game = turtle.Screen()
    game.title("Jumper AI")
    game.bgcolor("black")
    game.setup(width=GAME_WIDTH, height=GAME_HEIGHT)
    game.tracer(0)
    createStatus()
    return game


def createStatus():
    status.speed(0)
    status.shape("square")
    status.color("gray")
    status.penup()
    status.hideturtle()
    status.goto(-(GAME_WIDTH / 2) + 50,
                -(GAME_HEIGHT / 2) + 20)
    status.write("---")


def showStatus(text):
    status.clear()
    status.write(text, font=("Courier", 16, "normal"))
