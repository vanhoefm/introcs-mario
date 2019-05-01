import os
path = os.getcwd()

class Creature:
    def __init__(self, x, y, radius, img, frame_width, frame_height, num_frames):
        self.x = x
        self.y = y
        self.vy = 0 # Velocity up or down
        self.vx = 0 # Velocity left or right
        self.radius = radius
        self.img = loadImage(path + "/images/" + img)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.curr_frame = 0
        self.direction = 1 # by default creature walks to the right

    def gravity(self):
        if self.y + self.radius < g.ground:
            # Our creature is falling down
            self.vy = self.vy + 0.3
        elif self.vy > 0:
            # Creature is on the ground
            self.vy = 0
        
        if self.y + self.radius + self.vy > g.ground:
            self.y = g.ground - self.radius
        else:
            self.y = self.y + self.vy

    def update(self):
        self.gravity()
    
    def display(self):
        self.update()
        
        ellipse(self.x, self.y, 2 * self.radius, 2 * self.radius)
        
        self.curr_frame = self.curr_frame + 0.2
        if self.curr_frame >= self.num_frames:
            self.curr_frame = 0
        
        offset_x1 = self.frame_width * int(self.curr_frame)
        offset_x2 = offset_x1 + self.frame_width
        if self.direction == -1:
            temp = offset_x1
            offset_x1 = offset_x2
            offset_x2 = temp
        
        image(self.img, self.x - self.frame_width//2, self.y - self.frame_height//2,
              self.frame_width, self.frame_height,
              offset_x1, 0, offset_x2, self.frame_height)

class Mario(Creature):
    def __init__(self, x, y, radius, img, frame_width, frame_height, num_frames):
        Creature.__init__(self, x, y, radius, img, frame_width, frame_height, num_frames)
        self.key_pressed = {LEFT: False, RIGHT: False, UP: False}
        
    def update(self):
        self.gravity()
        
        if self.key_pressed[LEFT]:
            self.direction = -1
            self.x -= 5
        elif self.key_pressed[RIGHT]:
            self.direction = 1
            self.x += 5
        
        if self.key_pressed[UP] and self.vy == 0:
            self.vy = -10


class Game:
    def __init__(self, width, height, ground):
        self.width = width
        self.height = height
        self.ground = ground
        self.mario = Mario(100, 100, 35, "mario.png", 100, 70, 11)
        self.bgImg = []
        
        for i in range(1, 6):
            img = loadImage(path + "/images/layer_0" + str(i) + ".png")
            self.bgImg.append(img)

    def display(self):
        for img in self.bgImg[::-1]:
            image(img, 0, 0)
        
        stroke(255)
        line(0, self.ground, self.width, self.ground)
        
        self.mario.display()
        
    def handle_keypress(self):
        if keyCode == LEFT:
            self.mario.key_pressed[LEFT] = True
        elif keyCode == RIGHT:
            self.mario.key_pressed[RIGHT] = True
        elif keyCode == UP:
            self.mario.key_pressed[UP] = True
            
    def handle_keyrelease(self):
        if keyCode == LEFT:
            self.mario.key_pressed[LEFT] = False
        elif keyCode == RIGHT:
            self.mario.key_pressed[RIGHT] = False
        elif keyCode == UP:
            self.mario.key_pressed[UP] = False

g = Game(1280, 720, 585)

def setup():
    size(g.width, g.height)

def draw():
    background(0)
    g.display()
    
def keyPressed():
    g.handle_keypress()

def keyReleased():
    g.handle_keyrelease()
