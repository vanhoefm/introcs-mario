import os, math
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
        #print(self.ground)
        
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
        
        #ellipse(self.x - g.screen_start_x, self.y, 2 * self.radius, 2 * self.radius)
        
        if self.vx != 0 or isinstance(self, Star):
            self.curr_frame = self.curr_frame + 0.3
            if self.curr_frame >= self.num_frames:
                self.curr_frame = 0
            
        offset_x1 = self.frame_width * int(self.curr_frame)
        offset_x2 = offset_x1 + self.frame_width
        if self.direction == -1:
            temp = offset_x1
            offset_x1 = offset_x2
            offset_x2 = temp
        
        image(self.img, self.x - self.frame_width//2 - g.screen_start_x, self.y - self.frame_height//2,
              self.frame_width, self.frame_height,
              offset_x1, 0, offset_x2, self.frame_height)
    
    def distance(self, other):
        return ( (self.x - other.x)**2 + (self.y - other.y)**2 )**0.5

class Mario(Creature):
    def __init__(self, x, y, radius, img, frame_width, frame_height, num_frames):
        Creature.__init__(self, x, y, radius, img, frame_width, frame_height, num_frames)
        self.key_pressed = {LEFT: False, RIGHT: False, UP: False}
        self.sound_jump = audioPlayer.loadFile(path + "/sounds/jump.mp3")
        self.sound_dies = audioPlayer.loadFile(path + "/sounds/gameover.wav")
        self.sound_kill = audioPlayer.loadFile(path + "/sounds/kill.mp3")
        self.sound_coin = audioPlayer.loadFile(path + "/sounds/coin.mp3")
        
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

        if self.x + self.vx > 0:
            self.x += self.vx
            if self.x > g.width // 2:
                g.screen_start_x += self.vx
                    
        if self.key_pressed[UP] and self.vy == 0:
            self.vy = -10
            self.sound_jump.rewind()
            self.sound_jump.play()
        
        for enemy in g.enemies:
            if self.distance(enemy) <= self.radius + enemy.radius:
                if self.vy > 0:
                    g.enemies.remove(enemy)
                    self.vy = -10
                    self.sound_kill.rewind()
                    self.sound_kill.play()
                else:
                    g.state = "pause"
                    self.sound_dies.rewind()
                    self.sound_dies.play()
                    
        for star in g.stars:
            if self.distance(star) <= self.radius + star.radius:
                g.stars.remove(star)
                self.sound_coin.rewind()
                self.sound_coin.play()

class Goomba(Creature):
    def __init__(self, x, y, radius, img, frame_width, frame_height, num_frames, edge_right, edge_left):
        Creature.__init__(self, x, y, radius, img, frame_width, frame_height, num_frames)
        self.edge_right = edge_right
        self.edge_left = edge_left
        self.vx = 3
        self.direction = 1
        
    def update(self):
        self.gravity()
        
        if self.x + self.vx > self.edge_left:
            # Make it walk to the right instead
            self.vx = -self.vx
            self.direction = -1
        elif self.x + self.vx < self.edge_right:
            # Make it walk to the left instead
            self.vx = -self.vx
            self.direction = 1
        
        self.x += self.vx

class Fire(Creature):
    def __init__(self, x, y, radius, img, frame_width, frame_height, num_frames, direction):
        Creature.__init__(self, x, y, radius, img, frame_width, frame_height, num_frames)
        self.direction = direction
        if direction == 1:
            self.vx = 10
        else:
            self.vx = -10
        self.time_remaining = 40

    def update(self):
        self.time_remaining -= 1
        if self.time_remaining == 0:
            g.fires.remove(self)
            return
        
        self.x += self.vx
        
        for enemy in g.enemies:
            if self.distance(enemy) <= self.radius + enemy.radius:
                g.enemies.remove(enemy)
                g.fires.remove(self)
                
                g.mario.sound_kill.rewind()
                g.mario.sound_kill.play()

class Star(Creature):
    def __init__(self, x, y, radius, img, frame_width, frame_height, num_frames, radius_circle, initial_angle):
        Creature.__init__(self, x, y, radius, img, frame_width, frame_height, num_frames)
        self.center_x = x
        self.center_y = y
        self.radius_circle = radius_circle
        self.angle = initial_angle
    
    def update(self):
        self.x = self.center_x + math.cos(self.angle) * self.radius_circle
        self.y = self.center_y + math.sin(self.angle) * self.radius_circle
        
        self.angle += 0.02

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/images/platform.png")
    
    def display(self):
        image(self.img, self.x - g.screen_start_x, self.y)

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
        self.enemies = []
        self.screen_start_x = 0
        self.fires = []
        self.sound_fire = audioPlayer.loadFile(path + "/sounds/fire.wav")
        self.stars = []
        
        for i in range(1, 6):
            img = loadImage(path + "/images/layer_0" + str(i) + ".png")
            self.bgImg.append(img)
            
        for i in range(3):
            platform = Platform(300 + i * 200, 500 - i * 100, 200, 50)
            self.platforms.append(platform)
        for i in range(3):
            platform = Platform(1300 + i * 200, 400 - i * 100, 200, 50)
            self.platforms.append(platform)
            
        for i in range(3):
            goomba = Goomba(700 + i * 100, 200, 35, "goomba.png", 70, 70, 5, 600, 1000)
            self.enemies.append(goomba)
        for i in range(3):
            goomba = Goomba(1400 + i * 100, 200, 35, "goomba.png", 70, 70, 5, 1300, 1800)
            self.enemies.append(goomba)
        
        for i in range(10):
            star = Star(300, 300, 20, "star.png", 40, 40, 6, 150, 2 * PI / 10 * i)
            self.stars.append(star)
        
        self.buttons.append(Button("Start Game", self.width//2 - 100, self.height//2 - 50, 50, 250))
        self.buttons.append(Button("Instructions", self.width//2 - 100, self.height//2 + 50, 50, 250))

    def displayMenu(self):
        background(0)
        
        for button in self.buttons:
            button.display()

    def displayGame(self):
        background(0)
        for img in self.bgImg[::-1]:
            width_right = self.screen_start_x % self.width
            width_left = self.width - width_right # self.screen_start_x
            
            # Draws the image on the right
            image(img, 0, 0, width_left, self.height, width_right, 0, self.width, self.height)
            
            # Draw the image on the left
            image(img, width_left, 0, width_right, self.height, 0, 0, width_right, self.height)
        
        stroke(255)
        line(0, self.ground, self.width, self.ground)
        
        for platform in self.platforms:
            platform.display()
        for enemy in self.enemies:
            enemy.display()
        for fire in self.fires:
            fire.display()
        for star in self.stars:
            star.display()
        
        self.mario.display()

    def display(self):
        if self.state == "menu":
            self.displayMenu()
        elif self.state == "game":
            self.displayGame()
    
    def handle_fire(self):
        fire = Fire(self.mario.x, self.mario.y, 25, "fire.png", 50, 50, 10, self.mario.direction)
        self.fires.append(fire)
        self.sound_fire.rewind()
        self.sound_fire.play()
    
    def handle_keypress(self):
        if keyCode == LEFT:
            self.mario.key_pressed[LEFT] = True
        elif keyCode == RIGHT:
            self.mario.key_pressed[RIGHT] = True
        elif keyCode == UP:
            self.mario.key_pressed[UP] = True
        elif keyCode == ord(' '):
            self.handle_fire()
            
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
    #frameRate(30)
    size(g.width, g.height)

def draw():
    g.display()
    
def keyPressed():
    g.handle_keypress()

def keyReleased():
    g.handle_keyrelease()
    
def mousePressed():
    g.handle_mousepressed()
