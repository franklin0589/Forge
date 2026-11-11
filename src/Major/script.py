import Major.main as main
import random

class MyApp(main.SampleApp):
    def setup(self: main.App):
        self.canvas.create_text(400, 300, text="Hello, World!", font=("Helvetica", 32))

    def update(self: main.App):
        self.clear()


        x = [random.random()*self.WIDTH for i in range(100)]
        y = [random.random()*self.HEIGHT for i in range(100)]
        points = []
        for i in range(100):
            points.append(x[i])
            points.append(y[i])

        self.canvas.create_polygon(*points, fill="blue", smooth =True)
        # self.canvas.create_text(400, 300, text="Updated!", font=("Helvetica", 32))