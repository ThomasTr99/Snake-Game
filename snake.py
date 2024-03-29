from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 70
SPACE_SIZE = 50
BODY_SEGMENTS = 3
SNAKE_COLOR = "#01ff02"
FOOD_COLOR = "#FF0000"
BACKGROUND = "#000000"

class snake:
    def __init__(self):
        #The size of the snake's body will be the size of its segments which is 3
        self.body_size = BODY_SEGMENTS
        #empty list of coordinates
        self.coordinates = []
        #empty list of squares
        self.squares = []

        for i in range(0, BODY_SEGMENTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        #The food will appear within a random space within the defined space that we have provided
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE-1)) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE-1)) * SPACE_SIZE
        self.coordinates = [x, y]
        #Creating the actual food
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    #Checks if the snake has touched the food by using its coordinates
    if x == food.coordinates[0] and y == food.coordinates[1]:
        #Score increments 
        global score
        score += 1
        #Scoreboard is changed when the snake touches the food
        label.config(text="Score: {}".format(score))
        #Food is deleted, then the food function is called to replace it
        canvas.delete("food")
        food = Food()
    
    else:
        #Deletes the last square of the snake as it travels down
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    window.after(SPEED, next_turn, snake, food)



def change_direction(new_direction):
    global direction
    if new_direction == "left":
        #This is so we do not go back around after we change to a new direction
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

    
def check_collisions(snake):
    x,y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    else:
        return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("Courier", 50), text="LOSER YOU LOSE", fill="red", tag="gameover")



window = Tk()
window.title("Snake Game+")
window.resizable(False, False)

#Scoreboard
score = 0
direction = 'down'
label = Label(window, text="Score: {}".format(score), font=("Courier", 40))
label.pack()

#Game Window
canvas = Canvas(window, bg=BACKGROUND, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Key Bindings
window.bind("<a>", lambda event: change_direction("left"))
window.bind("<d>", lambda event: change_direction("right"))
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<s>", lambda event: change_direction("down"))

snake = snake()
food = Food()

next_turn(snake, food)


window.mainloop()