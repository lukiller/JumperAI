import turtle
import jumper


class Ground:
    def createGround():
        ground = turtle.Turtle()
        ground.speed(0)
        ground.pensize(3)
        ground.shape("square")
        ground.color("brown")
        ground.penup()
        ground.goto(-jumper.STARTX, jumper.GROUND)
        ground.pendown()
        ground.goto(jumper.STARTX, jumper.GROUND)
        ground.penup()
        return ground
