


class ObjectPlacement:
    def __init__(self, obj:int, position: tuple[float, float], time:int):
        self.obj = obj
        self.position = position
        self.time = time

class Grid:
    def __init__(self):
        self.origin = (2, 2)
        self.min_bound = (0.0, 0.0)
        self.max_bound = (0.0, 0.0)
        self.width = 5
        self.height = 5

        self.elements = {}

    def add_element(self, position: tuple[int, int], element: str):
        self.elements[position] = element

    def set_bounds(self, min_bound: tuple[int, int], max_bound: tuple[int, int]):
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.width = max(self.width, 2*(self.max_bound[0] - self.min_bound[0]))
        self.height =max(self.height, 2*(self.max_bound[1] - self.min_bound[1]))

    def __repr__(self):
        representation = "{:<3}".format("x")
        for j in range(self.width):
            representation += f"{j-self.origin[0]:^4}"
        representation += "\n"

        for i in range(self.height):
            representation += "{:^3}".format(i-self.origin[1])
            for j in range(self.width):
                char = "."
                char =  "=" if i == self.origin[0] else char
                char =  "|" if j == self.origin[1] else char
                char =  "o" if i == self.origin[0] and j == self.origin[1] else char

                if (i-self.origin[0], j-self.origin[0]) in self.elements:
                    char = self.elements[(i-self.origin[0], j-self.origin[1])]
                representation += "{:^4}".format(char)
            representation += "\n"
        return representation
    
class Scene:
    def __init__(self):
        self.grid = Grid()
        self.objects : list[ObjectPlacement] = []

    def add_object(self, obj: ObjectPlacement):
        self.objects.append(obj)
        self.grid.add_element((int(obj.position[0]), int(obj.position[1])), f"X")
        self.define_bounds()

    def define_bounds(self):
        if not self.objects:
            return
        min_x = int(min(obj.position[0] + self.grid.origin[0] for obj in self.objects))
        min_y = int(min(obj.position[1] + self.grid.origin[1] for obj in self.objects))
        max_x = int(max(obj.position[0] + self.grid.origin[0] for obj in self.objects))
        max_y = int(max(obj.position[1] + self.grid.origin[1] for obj in self.objects))
        self.grid.set_bounds((min_x, min_y), (max_x, max_y))

    def view(self):
        for obj in self.objects:
            print(f"Object ID: {obj.obj}, Position: {obj.position}, Time: {obj.time}")
        print("Grid Representation:")
        print(self.grid)
        
        

def main():
    # Entry point for the placement module.
    # Implement the placement logic here.
    scene = Scene()
    obj1 = ObjectPlacement(1, (0.0, 0.0), 4)
    obj2 = ObjectPlacement(2, (3.0, 3.0), 5)
    scene.add_object(obj1)
    scene.add_object(obj2)
    scene.view()
    

    pass



if __name__ == "__main__":
    main()