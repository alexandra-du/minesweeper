import random
import numpy as np
from tkinter import *

# create array of size m*n, for example:
m=10
n=10
array = np.zeros((m,n))
#the first and last rows, and the first and last columns, are only used for boundary conditions

#place bombs: 1) each cell contains a bomb with given probability, for example
p = 0.2
for i in range(1,m-1):
    for j in range(1,n-1):
        array[i][j] = (random.random() < p)
        
        
#solve the game by computing for each cell the nb of bombs contained in the 
#nearest neighboring cells
solutions = np.zeros((m,n))
for i in range(1,m-1):
    for j in range(1,n-1):
        if not(array[i][j]):
            #corresponding cell of solutions contains the nb of bombs near it
            solutions[i][j] = np.sum(array[i-1:i+2,j-1:j+2])
        else:
            #if cell contains a bomb, value will be 10 (arbitrarily)
            solutions[i][j] = 10

            
            
class Minesweeper:

    def __init__(self, master):
        
        # set up frame
        frame = Frame(master)
        frame.pack()
        
        # possible states of a cell: unclicked; clicked; flag placed on it, + others ?
        self.flags = 0
        self.clicked = 0
        
        self.mines = np.sum(array)
            
        self.buttons = dict({})
        x_coord = 1
        y_coord = 1

        for x in range((n-2)*(m-2)):
            mine = 0
            message = "    "
            self.buttons[x] = [ Button(frame, text=message), #initial state of button at beginning of game
                                mine, #contains bomb or not (0/1)
                                0, #state of cell (0: unclicked, 1: clicked, 2: flagged)
                                x, #ID of cell
                                [x_coord, y_coord], #coordinates of cell
                                0 ] #number of adjacent bombs
            
            #print(x_coord, y_coord)
            
            #assign a mine to the cell or not
            self.buttons[x][1] = (solutions[x_coord][y_coord]==10)
            
            #in the event of a right click:    
            self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))
            
            #in the event of a left click:
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            
            #nb of adjacent bombs:
            self.buttons[x][5] = solutions[x_coord][y_coord]
            
            # calculate coords:
            if y_coord == n-2:
                y_coord = 0
                x_coord += 1
            y_coord += 1
        
        #create the grid with buttons after each turn
        for key in self.buttons:
            self.buttons[key][0].grid(row = self.buttons[key][4][0], column = self.buttons[key][4][1])
               
                
    #details for in the event of a right click:            
    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(self.buttons[x])      
    
    def rclicked(self, button_data):
        # if not clicked
        if button_data[2] == 0:                  #if button is unclicked
            button_data[0].config(text='flag')
            button_data[2] = 2
         
        # if flagged, unflag
        elif button_data[2] == 2:
            button_data[0].config(text='    ')
            button_data[2] = 0
        
    #details in the event of a left click:
    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(self.buttons[x])

    def lclicked(self, button_data):
        if button_data[1] == 1: #if a mine
            # show all mines and check for flags
            for key in self.buttons:
                #for all mines that were not flagged
                if self.buttons[key][1] == 1 and self.buttons[key][2] == 0:
                    self.buttons[key][0].config(background = 'red')
                #for all flagged mines
                if self.buttons[key][1] == 1 and self.buttons[key][2] == 2:
                    self.buttons[key][0].config(background = 'green')
                #for all flagged but are not mines
                if self.buttons[key][1] != 1 and self.buttons[key][2] == 2:
                    self.buttons[key][0].config(text = ' X ')
            # end game
            self.gameover()
        else:
            #if the clicked cell has no neighboring mine
            if button_data[5] == 0:
                button_data[0].config(background = 'white')
                #unveil all neighboring cells and so on (to be continued)
                
            else:
                button_data[0].config(background = 'white', text = ' ' + str(int(button_data[5])) + ' ')
            # if not already set as clicked, change state and count
            if button_data[2] != 1:
                button_data[2] = 1
                self.clicked += 1
            if self.clicked == (m-2)*(n-2) - self.mines:
                for key in self.buttons:
                #for all mines that were correctly flagged
                    if self.buttons[key][2] == 2:
                        self.buttons[key][0].config(background = 'green')
                self.victory()
                
    def gameover(self):
        global top
        messagebox.showinfo("Info", "Game over")
        top.destroy()
        
    def victory(self):
        messagebox.showinfo("Info", "You Win!")
        global top
        top.destroy() 
           
        
#-----------------------------------------------------------------------------------------------------------
def main():
    # create Tk widget
    global top
    top = Tk()
    # set program title
    top.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(top)
    # run event loop
    top.mainloop()
if __name__ == "__main__":
    main()
