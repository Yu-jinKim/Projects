from tkinter import *
import random

fenetre = Tk()

height = 250
width = 250

def change_dir(event):
    touche = event.keysym

    if touche == "Up":
        move_snake(0, -25)
    elif touche == "Down":
        move_snake(0, 25)
    elif touche == "Right":
        move_snake(25, 0)
    elif touche == "Left":
        move_snake(-25, 0)

def move_snake(x, y):
    canvas.move(rectangle, x, y)
    fenetre.after(500, move_snake)

# création du canvas
canvas = Canvas(fenetre, width=width, height=height, bg="ivory")
# création du rectangle
rectangle = canvas.create_rectangle(height/2,width/2,height/2+25,width/2+25,fill="violet")
food_x = random.randrange(0, width-25, 25)
food_y = random.randrange(0, height-25, 25)
food = canvas.create_oval(food_x, food_y, food_x+25, food_y+25, fill="yellow")

canvas.focus_set()
canvas.bind("<Key>", change_dir)

canvas.pack()

fenetre.mainloop()