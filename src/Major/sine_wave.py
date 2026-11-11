import Major.main as main
import random
import tkinter as tk


class Ball:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, canvas:tk.Canvas):
        r_size = self.size//2
        canvas.create_oval(int(self.x - r_size), int(self.y - r_size), int(self.x + r_size), int(self.y + r_size), outline="red", fill="red")

class MyApp(main.SampleApp):
    def setup(self: main.App):
        self.canvas.create_text(400, 300, text="Hello, World!", font=("Helvetica", 32))
        self.balls = []
        for b in range(1000):
            self.ball = Ball(100, 100, 5)
            self.ball.x = (b/1000)*self.WIDTH
            self.ball.y = self.sine(b/1000, 0)*50+ self.HEIGHT/2
            self.ball.draw(self.canvas)
            self.balls.append(self.ball)


    def update(self: main.App):
        self.clear()
        # print(self.ball.x)
        for b in range(1000):
            self.balls[b].y = self.sine(b/1000, 15*self.TWO_PI*self.tick())*50 + self.HEIGHT/2
            self.balls[b].draw(self.canvas)