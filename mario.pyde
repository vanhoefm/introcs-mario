import os
path = os.getcwd()

class Creature:
    def __init__(self, x, y, radius, img, frame_width, frame_height):
        self.x = x
        self.y = y
        self.vy = 0 # Velocity up or down
        self.vx = 0 # Velocity left or right
        self.radius = radius
        self.img = loadImage(path + "/images/" + img)
        self.frame_width = frame_width
        self.frame_height = frame_height

    def update(self):
        if self.y + self.radius < g.ground:
            # Our creature is falling down
            self.vy = self.vy + 0.3
        else:
            # Creature is on the ground
            self.vy = 0
        
        if self.y + self.radius + self.vy > g.ground:
            self.y = g.ground - self.radius
        else:
            self.y = self.y + self.vy

    def display(self):
        self.update()
        
        ellipse(self.x, self.y, 2 * self.radius, 2 * self.radius)
        image(self.img, self.x - self.frame_width//2, self.y - self.frame_height//2,
              self.frame_width, self.frame_height,
              0, 0, self.frame_width, self.frame_height)

class Game:
    def __init__(self, width, height, ground):
        self.width = width
        self.height = height
        self.ground = ground
        self.mario = Creature(100, 100, 35, "mario.png", 100, 70)

    def display(self):
        stroke(255)
        line(0, self.ground, self.width, self.ground)
        
        self.mario.display()

g = Game(1280, 720, 600)

def setup():
    size(g.width, g.height)

def draw():
    background(0)
    g.display()
