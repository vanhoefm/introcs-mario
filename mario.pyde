
class Game:
    def __init__(self, width, height, ground):
        self.width = width
        self.height = height
        self.ground = ground

g = Game(1280, 720, 600)

def setup():
    size(g.width, g.height)

def draw():
    background(0)
    stroke(255)
    line(0, g.ground, g.width, g.ground)
