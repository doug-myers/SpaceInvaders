# Space Invaders

import turtle
import math
import platform

print(platform.system())
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available.")


# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.setup(width=600, height=600)
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

# Register the shapes
wn.register_shape("invader.gif")
wn.register_shape("player.gif")

# Set the score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("light blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

playerspeed = 15

number_of_enemies = 30
enemies = []

y = 300
for i in range(number_of_enemies):
    # Create the enemy
    enemy = turtle.Turtle() 
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    if i % 10 == 0:
        x = -225
        y -= 50
    else:
        x += 50
    enemy.setposition(x, y)
    enemies.append(enemy)

enemyspeed = 0.1


# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 3

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

# Move the palyer left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
      x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
      x = 280
    player.setx(x)

def fire_bullet():
    # Decleare bulletstate as a blobal if it it needs changed
    global bulletstate

    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()
        play_sound("Flash-laser-03.wav")

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False

def play_sound(sound_file, time = 0):
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    elif platform.system() == "Mac":
        os.system("afplay {}&".format(sound_file))

    # Reapeat sound
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))

# Create keyboard bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Play backgroun music
play_sound("space.wav", 73)

# Main game loop
gameover = False
while not gameover:
    wn.update()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the eneemy back and down
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            # Reset the bullet
            play_sound("Explosion+1.wav")
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            enemy.setposition(0, 10000)
            # Update the score
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))


        if isCollision(player,enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            gameover = True

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    
