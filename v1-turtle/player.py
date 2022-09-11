import turtle
import jumper


class Player:
    PLAYER_POSX = -(jumper.GAME_WIDTH / 2 - 50)
    PLAYER_WIDTH = 1
    PLAYER_HEIGHT = 3
    PLAYER_GROUND = jumper.GROUND + PLAYER_HEIGHT * jumper.TURTLE_SIZE / 2
    JUMP_HEIGHT = 15
    STATE_READY = "ready"
    STATE_JUMPING = "jumping"
    STATE_CROUCHING = "crouching"

    def createPlayer(self, offset, color):
        player = turtle.Turtle()
        player.speed(0)
        player.shape("square")
        player.shapesize(stretch_wid=Player.PLAYER_HEIGHT,
                         stretch_len=Player.PLAYER_WIDTH)
        player.width = Player.PLAYER_WIDTH * jumper.TURTLE_SIZE
        player.height = Player.PLAYER_HEIGHT * jumper.TURTLE_SIZE
        player.color(color)
        player.dy = 0
        player.penup()
        player.state = Player.STATE_READY
        player.gameOver = False
        player.goto(Player.PLAYER_POSX + offset, Player.PLAYER_GROUND)
        return player

    def movePlayer(self, player):
        player.dy += jumper.GRAVITY
        y = player.ycor()
        y += player.dy
        player.sety(y)
        if player.ycor() < self.getGround():
            player.sety(self.getGround())
            player.dy = 0
            if player.state == Player.STATE_JUMPING:
                player.state = Player.STATE_READY

    def jump(self, player):
        if player.state == Player.STATE_READY:
            player.dy = Player.JUMP_HEIGHT
            player.state = Player.STATE_JUMPING

    def crouch(self, player):
        if player.state == Player.STATE_READY:
            player.shapesize(stretch_wid=Player.PLAYER_WIDTH,
                             stretch_len=Player.PLAYER_HEIGHT)
            player.width = Player.PLAYER_HEIGHT * jumper.TURTLE_SIZE
            player.height = Player.PLAYER_WIDTH * jumper.TURTLE_SIZE
            player.state = Player.STATE_CROUCHING
            Player.PLAYER_GROUND = jumper.GROUND + \
                Player.PLAYER_WIDTH * jumper.TURTLE_SIZE / 2

    def standup(self, player):
        if player.state == Player.STATE_CROUCHING:
            player.shapesize(stretch_wid=Player.PLAYER_HEIGHT,
                             stretch_len=Player.PLAYER_WIDTH)
            player.width = Player.PLAYER_WIDTH * jumper.TURTLE_SIZE
            player.height = Player.PLAYER_HEIGHT * jumper.TURTLE_SIZE
            player.state = Player.STATE_READY
            Player.PLAYER_GROUND = jumper.GROUND + \
                Player.PLAYER_HEIGHT * jumper.TURTLE_SIZE / 2

    def collision(self, obj1, obj2):
        if (obj1.xcor() + obj1.width >= obj2.xcor() and
            obj1.xcor() <= obj2.xcor() + obj2.width and
            obj1.ycor() + obj1.height >= obj2.ycor() and
                obj1.ycor() <= obj2.ycor() + obj2.height):
            return True

    def getGround(self):
        return Player.PLAYER_GROUND
