import os
path = os.getcwd()
add_library("minim")
audioPlayer = Minim(this)

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
        self.ground = 0

    def determine_ground(self):
        self.ground = g.ground
        for p in g.platforms:
            if p.x <= self.x <= p.x + p.width and self.y + self.radius <= p.y:
                self.ground = p.y

    def gravity(self):
        self.determine_ground()
        print(self.ground)
        
        # Updates the speed of falling down
        if self.y + self.radius < self.ground:
            # Our creature is falling down
            self.vy = self.vy + 0.3
        elif self.vy > 0:
            # Creature is on the ground
            self.vy = 0
        
        # Detect collision with the ground, and actually fall down
        if self.y + self.radius + self.vy > self.ground:
            # If the creature would hit the ground, set location equal to the ground
            self.y = self.ground - self.radius
        else:
            # Creature doesn't yet hit the ground, so update location based
            # on the current speed of the creature.
            self.y = self.y + self.vy

    def update(self):
        self.gravity()
    
    def display(self):
        self.update()
        
        ellipse(self.x, self.y, 2 * self.radius, 2 * self.radius)
        
        if self.vx != 0:
            self.curr_frame = self.curr_frame + 0.3
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
        self.sound_jump = audioPlayer.loadFile(path + "/sounds/jump.mp3")
        
    def update(self):
        self.gravity()
        
        if self.key_pressed[LEFT]:
            self.direction = -1
            self.vx = -5
        elif self.key_pressed[RIGHT]:
            self.direction = 1
            self.vx = 5
        else:
            self.vx = 0

        self.x += self.vx
                
        if self.key_pressed[UP] and self.vy == 0:
            self.vy = -10
            self.sound_jump.rewind()
            self.sound_jump.play()

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/images/platform.png")
    
    def display(self):
        image(self.img, self.x, self.y)

class Button:
    def __init__(self, label, x, y, height, width):
        self.label = label
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    
    def contains_mouse(self):
        return self.x <= mouseX <= self.x + self.width and self.y - self.height <= mouseY <= self.y
    
    def display(self):
        #print(self.x, mouseX, self.x + self.width)
        if self.contains_mouse():
            #print("stroke is being called")
            fill(255, 0, 0)
        else:
            fill(255)
        textSize(40)
        text(self.label, self.x, self.y)

class Game:
    def __init__(self, width, height, ground):
        self.width = width
        self.height = height
        self.ground = ground
        self.mario = Mario(100, 100, 35, "mario.png", 100, 70, 11)
        self.bgImg = []
        self.state = "menu"
        self.buttons = []
        self.platforms = []
        
        for i in range(1, 6):
            img = loadImage(path + "/images/layer_0" + str(i) + ".png")
            self.bgImg.append(img)
            
        for i in range(3):
            platform = Platform(300 + i * 200, 500 - i * 100, 200, 50)
            self.platforms.append(platform)
            
        self.buttons.append(Button("Start Game", self.width//2 - 100, self.height//2 - 50, 50, 250))
        self.buttons.append(Button("Instructions", self.width//2 - 100, self.height//2 + 50, 50, 250))

    def displayMenu(self):
        background(0)
        
        for button in self.buttons:
            button.display()

    def displayGame(self):
        for img in self.bgImg[::-1]:
            image(img, 0, 0)
        
        stroke(255)
        line(0, self.ground, self.width, self.ground)
        
        for platform in self.platforms:
            platform.display()
        
        self.mario.display()

    def display(self):
        if self.state == "menu":
            self.displayMenu()
        else:
            self.displayGame()
        
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
            
    def handle_mousepressed(self):
        if self.buttons[0].contains_mouse():
            self.state = "game"

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
    
def mousePressed():
    g.handle_mousepressed()
