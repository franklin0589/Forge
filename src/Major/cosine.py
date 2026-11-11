import Major.main as main
import random
import tkinter as tk


class Ball:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = "red"  

    def draw(self, canvas:main.CanvasContextInterface):

        canvas.draw_circle((self.x, self.y), self.size, self.color)
    


class MyApp(main.SampleApp):
    def setup(self: main.App):
        self.balls = []
        self.green_balls = []
        for b in range(1000):
            
            self.ball = Ball(0, 0, 5)
            self.ball.x = (b/1000)*self.WIDTH - self.WIDTH/2
            ball_temp = Ball(self.ball.x,0, 5)
            ball_temp.color = "green"
            self.green_balls.append(ball_temp)
            self.ball.y = self.cosine(b/1000, 0)*50
            self.ball.draw(self.context)
            self.balls.append(self.ball)


    def update(self: main.App):
        self.clear()
        self.context.draw_text((0, 0), text="Hello, World!", font=("Helvetica", 32))
        # print(self.ball.x)
        for b in range(1000):
            sine_y = 25+self.sine(b/1000, self.TWO_PI*self.tick())*50
            # ball_temp = Ball(self.balls[b].x, sine_y, 5)
            # ball_temp.color = "blue"
            # ball_temp.draw(self.context)
            self.balls[b].y =25+self.cosine(b/1000, self.TWO_PI*self.tick())*50
            self.balls[b].draw(self.context)
            tan_y = 25+self.tan(b/1000, self.tick()/100)*50
            self.green_balls[b].y = tan_y
            self.green_balls[b].draw(self.context)