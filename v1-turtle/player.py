import turtle
from unittest.mock import DEFAULT
from jumper import Jumper


class Player:
    PLAYER_POSX = -(Jumper.GAME_WIDTH / 2 - 50)
    PLAYER_WIDTH = 1
    PLAYER_HEIGHT = 3
    JUMP_HEIGHT = 15
    DEFAULT_COLOR = "indianred"
    STATE_READY = "ready"
    STATE_JUMPING = "jumping"
    STATE_CROUCHING = "crouching"

    def createPlayer(self, color=DEFAULT_COLOR):
        player = turtle.Turtle()
        player.color(color)
        self.resetPlayer(player)
        return player

    def resetPlayer(self, player):
        previousColor = player.color()[0]
        player.reset()
        player.color(previousColor)
        player.speed(0)
        player.shape("square")
        player.shapesize(stretch_wid=Player.PLAYER_HEIGHT, stretch_len=Player.PLAYER_WIDTH)
        # The ground is in the middle of the player's height
        player.ground = Jumper.GROUND + Player.PLAYER_HEIGHT * Jumper.TURTLE_SIZE / 2
        player.width = Player.PLAYER_WIDTH * Jumper.TURTLE_SIZE
        player.height = Player.PLAYER_HEIGHT * Jumper.TURTLE_SIZE
        player.dy = 0
        player.penup()
        player.state = Player.STATE_READY
        player.action = Jumper.ACTION_NONE
        player.distance = 0
        player.gameOver = False
        player.goto(Player.PLAYER_POSX, player.ground)

    def movePlayer(self, player):
        player.dy += Jumper.GRAVITY
        y = player.ycor()
        y += player.dy
        player.sety(y)
        if player.ycor() < player.ground:
            player.sety(player.ground)
            player.dy = 0
            if player.state == Player.STATE_JUMPING:
                player.state = Player.STATE_READY

    def jump(self, player):
        if player.state == Player.STATE_READY:
            player.dy = Player.JUMP_HEIGHT
            player.state = Player.STATE_JUMPING
            player.action = Jumper.ACTION_NONE

    def crouch(self, player):
        if player.state == Player.STATE_READY:
            player.shapesize(stretch_wid=Player.PLAYER_WIDTH,
                             stretch_len=Player.PLAYER_HEIGHT)
            player.width = Player.PLAYER_HEIGHT * Jumper.TURTLE_SIZE
            player.height = Player.PLAYER_WIDTH * Jumper.TURTLE_SIZE
            player.state = Player.STATE_CROUCHING
            player.ground = Jumper.GROUND + Player.PLAYER_WIDTH * Jumper.TURTLE_SIZE / 2

    def standup(self, player):
        if player.state == Player.STATE_CROUCHING:
            player.shapesize(stretch_wid=Player.PLAYER_HEIGHT,
                             stretch_len=Player.PLAYER_WIDTH)
            player.width = Player.PLAYER_WIDTH * Jumper.TURTLE_SIZE
            player.height = Player.PLAYER_HEIGHT * Jumper.TURTLE_SIZE
            player.state = Player.STATE_READY
            player.ground = Jumper.GROUND + Player.PLAYER_HEIGHT * Jumper.TURTLE_SIZE / 2

    def collision(self, obj1, obj2):
        obj1.x = obj1.xcor() - (obj1.width / 2)
        obj2.x = obj2.xcor() - (obj2.width / 2)
        obj1.y = obj1.ycor() - (obj1.height / 2)
        obj2.y = obj2.ycor() - (obj2.height / 2)
        if (obj1.x + obj1.width >= obj2.x and
            obj1.x <= obj2.x + obj2.width and
            obj1.y + obj1.height >= obj2.y and
                obj1.y <= obj2.y + obj2.height):
            return True

    def nextPlayerAction(self, player, nextPossibleAction):
        # Status: R=ready, J=jumping, C=crouching
        # Action: J=jump, C=crouch, S=standup, N=none
        # currentPlayerStatus, nextPossibleAction -> nextAction
        # | R J J | J J - | C J J |
        # | R C C | J C - | C C C |
        # | R - - | J - - | C - S |
        currentPlayerStatus = player.state
        if currentPlayerStatus == Player.STATE_READY or currentPlayerStatus == Player.STATE_CROUCHING:
            if nextPossibleAction == Jumper.ACTION_JUMP or nextPossibleAction == Jumper.ACTION_CROUCH:
                return nextPossibleAction
        if currentPlayerStatus == Player.STATE_CROUCHING:
            return Jumper.ACTION_STANDUP
        return Jumper.ACTION_NONE
