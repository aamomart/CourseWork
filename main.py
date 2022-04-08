# Import required libraries
from tkinter import *
import turtle as t
import keyboard as k
import time

# LIST OF ATTRIBUTES 4 LEVEL:
# player, platform1, platform2, patrol, platform3, goal, platform4, levelExit, fly

level1Atr = [[0,0,20,50, "blue"], [0,-35,100,20,"green"], [240,100,150,20,"green"], [240,120,20,20,"red"], [450,200,100,20,"green"], [450,220,20,20, "yellow"], [-200,100,100,20,"green"], [-200,135,20,50,"yellow"], [-1000,-1000,20,20, "red"]]

level2Atr = [[-400,-200,20,50, "blue"], [-400,-235,100,20,"green"], [250,100,150,20,"green"], [250,120,20,20,"red"], [450,200,100,20,"green"], [450,220,20,20, "yellow"], [-180,100,100,20,"green"], [-180,135,20,50,"yellow"], [-1000,-1000,20,20, "red"]]

compLvl1 = False
compLvl2 = False

def level1():
    # Set variables
    playerSpeed = 3
    flySpeed = 2
    patrolSpeed = 4
    found = False
    player_dy = 0
    terminal_velocity = -30
    gravity = -0.5
    playerJump = 12
    can_jump = False
    comp = run(level1Atr, playerSpeed, flySpeed, patrolSpeed, found, player_dy, terminal_velocity, gravity, playerJump, can_jump)
    if comp == True:
        global compLvl1
        compLvl1 = True
    
def level2():
    # Set variables
    if compLvl1 == False:
        newWindow = Toplevel(master)
        newWindow.configure(bg = 'black')
        popupMsg = Label(newWindow, text = "Need to complete previous level", fg = 'white', bg = 'black', font = ('Arial', 50))
        popupMsg.pack(pady = 50, padx = 10)
    else:
        playerSpeed = 3
        flySpeed = 2
        patrolSpeed = 4
        found = False
        player_dy = 0
        terminal_velocity = -30
        gravity = -0.25
        playerJump = 12
        can_jump = False
        level = 2
        run(level2Atr, playerSpeed, flySpeed, patrolSpeed, found, player_dy, terminal_velocity, gravity, playerJump, can_jump)

def run(levelAtr, playerSpeed, flySpeed, patrolSpeed, found, player_dy, terminal_velocity, gravity, playerJump, can_jump):

    # Set turtle conditions
    t.hideturtle()
    t.tracer(0, 0)
    t.bgcolor(0,0,0)
    
    # Set screen style
    screen = t.Screen()
    screen.setup(width = 1.0, height = 1.0)

    # Create transform class to store variables used for collisions because I don't want to have to keep retyping them
    class Transform:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

    # Create function to check for collsions, take parameters from transform class
    def rectCollision(transform1, transform2):   
        Collide = False
        tWidth = (transform1.width/2)+(transform2.width/2)
        tHeight = (transform1.height/2)+(transform2.height/2)
        xDistance = abs(transform2.x-transform1.x)
        yDistance = abs(transform2.y-transform1.y)
        if xDistance < tWidth and yDistance < tHeight:
            Collide = True
        else:
            pass
        return Collide

    # Create a function to resolve a collision with a platform
    def resolve_collision(player, platform):
        # While the player is colliding with the platform
        while rectCollision(player.transform, platform.transform):
            # Move them up by gravity to counteract gravity
            player.transform.y -= gravity

    # Create renderer class, use turtle to create generic rectangle
    class Renderer:
        def renderRectangle(self, rect):
            y = rect.transform.y - rect.transform.height/2
            t.penup()
            t.goto(rect.transform.x, y)
            t.pendown()
            t.fillcolor(rect.colour)
            t.begin_fill()
            t.forward(rect.transform.width/2)
            t.left(90)
            t.forward(rect.transform.height)
            t.left(90)
            t.forward(rect.transform.width)
            t.left(90)
            t.forward(rect.transform.height)
            t.left(90)
            t.forward(rect.transform.width/2)
            t.end_fill()

    # Create class to create objects of Renderer
    class Rectangle:
        def __init__(self, transform, colour):
            self.transform = transform
            self.colour = colour

    def initials():
        global player, platform1, platform2, patrol, platform3, goal, platform4, levelExit, fly
        player = Rectangle(Transform(levelAtr[0][0],levelAtr[0][1],levelAtr[0][2],levelAtr[0][3]),levelAtr[0][4])
        platform1 = Rectangle(Transform(levelAtr[1][0],levelAtr[1][1],levelAtr[1][2],levelAtr[1][3]),levelAtr[1][4])
        platform2 = Rectangle(Transform(levelAtr[2][0],levelAtr[2][1],levelAtr[2][2],levelAtr[2][3]),levelAtr[2][4])
        patrol = Rectangle(Transform(levelAtr[3][0],levelAtr[3][1],levelAtr[3][2],levelAtr[3][3]),levelAtr[3][4])
        platform3 = Rectangle(Transform(levelAtr[4][0],levelAtr[4][1],levelAtr[4][2],levelAtr[4][3]),levelAtr[4][4])
        goal = Rectangle(Transform(levelAtr[5][0],levelAtr[5][1],levelAtr[5][2],levelAtr[5][3]),levelAtr[5][4])
        platform4 = Rectangle(Transform(levelAtr[6][0],levelAtr[6][1],levelAtr[6][2],levelAtr[6][3]),levelAtr[6][4])
        levelExit = Rectangle(Transform(levelAtr[7][0],levelAtr[7][1],levelAtr[7][2],levelAtr[7][3]),levelAtr[7][4])
        fly = Rectangle(Transform(levelAtr[8][0],levelAtr[8][1],levelAtr[8][2],levelAtr[8][3]),levelAtr[8][4])

    # Create objects
    renderer = Renderer()
    initials()

    # Create an array of platforms for the plat loop
    platforms = [platform1, platform2, platform3, platform4]
    
    time.sleep(1)

    # Game loop
    while True:

        # Renew GUI every frame
        t.clear()

        # Render player, fly and goal every frame
        renderer.renderRectangle(player)
        renderer.renderRectangle(fly)
        renderer.renderRectangle(patrol)
        for plat in platforms:
            renderer.renderRectangle(plat)

        # Check if player has found goal, if yes then render level exit
        if found:
            renderer.renderRectangle(levelExit)

        # If no then render goal
        else:
            renderer.renderRectangle(goal)

        # Check if at terminal velocity, if no apply gravity
        if player_dy > terminal_velocity:
            player_dy += gravity

        # Move the player by their dy speed
        player.transform.y += player_dy

        # By default don't let the player jump
        can_jump = False

        # Check if player is moving down
        if player_dy < 0:

            # Check for a collision with plat, if yes resolve collision
            for plat in platforms:
                if rectCollision(player.transform, plat.transform):
                    can_jump = True
                    resolve_collision(player, plat)
                    player_dy = 0
                    break

        # Check if player has collided with fly, if yes then reset variables
        if rectCollision(player.transform, fly.transform) or player.transform.y < -1500 or rectCollision(player.transform, patrol.transform):
            t.bgcolor("red")
            time.sleep(0.05)
            initials()
            found = found = False
            t.bgcolor(0,0,0)

        # Check if player has collided with goal, if yes then hide goal 
        if rectCollision(player.transform, goal.transform):
            found = True

        # Check if player has collided with level exit and has found goal, if yes end game
        if rectCollision(player.transform, levelExit.transform) and found == True:
            t.bgcolor("yellow")
            time.sleep(0.05)
            initials()
            found = False
            t.bye()
            return True

        # Check for user input and reset player coordinates accordingly
        try:
            if k.is_pressed('Right') or k.is_pressed('d'):
                player.transform.x += playerSpeed
            if k.is_pressed('Left') or k.is_pressed('a'):
                player.transform.x -= playerSpeed
            if (k.is_pressed('Up') or k.is_pressed('w') or k.is_pressed('Space'))and can_jump == True:
                player_dy = playerJump
            if k.is_pressed('esc'):
                t.bye()
                return False
        except:
            pass

        # Check for player location in comparison to fly and reset fly coordinates accordingly
        if player.transform.x > fly.transform.x:
            fly.transform.x += flySpeed
        if player.transform.x < fly.transform.x:
            fly.transform.x -= flySpeed
        if player.transform.y > fly.transform.y:
            fly.transform.y += flySpeed
        if player.transform.y < fly.transform.y:
            fly.transform.y -= flySpeed
            
        # Make patrol turn at end of platform
        if (patrol.transform.x > (platform2.transform.x + (platform2.transform.width/2 - patrol.transform.width/2))) or (patrol.transform.x < (platform2.transform.x - (platform2.transform.width/2 - patrol.transform.width/2))):
            patrolSpeed = -patrolSpeed
            
        # Start patrol patrolling
        patrol.transform.x += patrolSpeed

        t.update()

        # Create frame rate
        time.sleep(1/60)

master = Tk()

master.geometry("3000x3000")
master.configure(bg = 'black')

label1 = Label(master, text = "Jump game", font = ('Arial', 40, 'bold'))
label1.pack(pady = 15)

button1 = Button(master, text = "Level 1", font = ('Arial', 20), command = level1)
button1.pack(pady = 10)

button1 = Button(master, text = "Level 2", font = ('Arial', 20), command = level2)
button1.pack(pady = 10)

mainloop()