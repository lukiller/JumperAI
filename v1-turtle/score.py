import turtle
from jumper import Jumper


class Score:
    def __init__(self):
        score = turtle.Turtle()
        score.speed(0)
        score.shape("square")
        score.color("gray")
        score.penup()
        score.hideturtle()
        score.goto(-(Jumper.GAME_WIDTH / 2) + 50, (Jumper.GAME_HEIGHT / 2) - 50)
        score.write("Distance 0m", font=("Courier", 24, "normal"))
        self.score = score

    def showScore(self, meters, generation=None):
        if meters % 10 == 0:
            self.score.clear()
            if generation == None:
                self.score.write(f"Distance {meters}m", font=("Courier", 24, "normal"))
            else:
                self.score.write(f"Generation {generation} - Distance {meters}m", font=("Courier", 24, "normal"))

    def showFinish(self, meters, generation=None):
        self.score.clear()
        if generation == None:
            self.score.write(f"GAME OVER (Distance {meters}m)", font=("Courier", 24, "normal"))
        else:
            self.score.write(f"GAME OVER (Generation {generation}, Distance {meters}m)", font=("Courier", 24, "normal"))
