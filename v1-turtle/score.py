import turtle
import jumper


class Score:
    def __init__(self):
        score = turtle.Turtle()
        score.speed(0)
        score.shape("square")
        score.color("gray")
        score.penup()
        score.hideturtle()
        score.goto(-(jumper.GAME_WIDTH / 2) + 50,
                   (jumper.GAME_HEIGHT / 2) - 50)
        score.write("Distance 0m", font=("Courier", 24, "normal"))
        self.score = score

    def showScore(self, meters):
        if meters % 10 == 0:
            self.score.clear()
            self.score.write(f"Distance {meters}m",
                             font=("Courier", 24, "normal"))
