from tkinter import *
import random

width = 500
height = 500

class Game:

    def __init__(self):
        self.fenetre = Tk()

        self.c = Canvas(self.fenetre, width=width, height=height, bg="ivory")
        self.c.grid()

        self.ship = self.c.create_rectangle(height/2,width-30,height/2+25,width-5,fill="violet")

        self.lasers = []

        def keys(event):
            touche = event.keysym
            coor_ship = self.c.coords(self.ship)

            if touche == "space":
                shooting(coor_ship)
            elif touche == "Right" and coor_ship[2] != 500:
                self.c.move(self.ship, 25, 0)
            elif touche == "Left" and coor_ship[0] != 0:
                self.c.move(self.ship, -25, 0)
            elif touche == "Escape":
                self.fenetre.destroy()
            # elif touche == "Right" and touche == "space":
            #     shooting(coor_ship)
            #     self.c.move(self.ship, 25, 0)
            # elif touche == "Left" and touche == "space":
            #     shooting(coor_ship)
            #     self.c.move(self.ship, -25, 0)

        def shooting(coor):
            self.laser = self.c.create_line(coor[0]+12.5, coor[3]-25, coor[0]+12.5, coor[3]-50)
            self.lasers.append(self.laser)
            move_lasers()

        def move_lasers():
            for self.laser in self.lasers:
                x0, y0, x1, y1 = self.c.coords(self.laser)
                if y0 > 200:
                    self.c.move(self.laser, 0, -25)
                else:
                    self.c.delete(self.laser)
                    self.lasers.remove(self.laser)
                    self.c.after_cancel(move_lasers)
            self.c.after(200, move_lasers)


        self.c.bind("<Key>", keys)
        self.c.focus_set()

        self.fenetre.mainloop()

Game()