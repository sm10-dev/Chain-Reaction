# Python program for 2 player version of the android game chain reaction using tkinter
import tkinter as tki

def move(win):
    win.grid[2][2].setOwner(1)
    win.grid[2][2].addOrb()
    win.grid[2][2].draw()   
    win.changePlayer()
    win.drawGrid()

class Grid():
    def __init__(self, canvas, xVal, yVal):
        self.capacity = self.getCapacity(xVal, yVal)      #sets the capacity of the grid
        self.owner = 9                          #default owner of grid is nobody
        self.orb = 0                            #holds the number of orbs in the cell
        self.posX = xVal                        #holds x coordinate of the grid 
        self.posY = yVal                        #holds y coordinate of the grid
        self.canvas = canvas                       #holds the canvas for drawing purposes
        
    def getCapacity(self,x,y):
        '''
        returns the capacity of the grid according to
        coordinates of the grid
        '''
        if(x == 0 or x == 7) and (y == 0 or y == 7):
            return 1
        elif (x == 0 or x == 7 or y == 0 or y == 7):
            return 2
        else:
            return 3
        
    def addOrb(self):
        '''
        Adds an orb to the grid and returns if split happened or not
        '''
        self.orb += 1
        if(self.orb == self.capacity+1):
            self.split()
            self.orb = 0
            return True
        
        return False
    
    def setOwner(self, val):
        '''
        sets the owner of the grid
        '''
        self.owner = val
        
    def changeOwner(self):
        '''
        changes the owner of the grid
        '''
        if(self.owner == 1):
            self.owner = 2
        elif(self.owner == 2):
            self.owner = 1
            
    def getColor(self):
        '''
        Returns color for drawing orbs according to
        the owner of the grid
        '''
        if(self.owner == 1):
            return 'green'
        elif(self.owner == 2):
            return 'red'
        
    def draw(self):
        '''
        function to draw orbs inside the grid
        '''
        col = self.getColor()
        if(self.orb == 1):
            self.canvas.create_oval(self.posX*50+15, self.posY*50+15,self.posX*50+35, self.posY*50+35,fill=col, width=1)
        elif(self.orb == 2):
            self.canvas.create_oval(self.posX*50+15, self.posY*50+15,self.posX*50+35, self.posY*50+35,fill='black', width=1)
            self.canvas.create_oval(self.posX*50+10, self.posY*50+10,self.posX*50+30, self.posY*50+30,fill=col, width=1)
            self.canvas.create_oval(self.posX*50+20, self.posY*50+20,self.posX*50+40, self.posY*50+40,fill=col, width=1)
        elif(self.orb == 3):
            self.canvas.create_oval(self.posX*50+10, self.posY*50+10,self.posX*50+30, self.posY*50+30,fill='black', width=1)
            self.canvas.create_oval(self.posX*50+20, self.posY*50+20,self.posX*50+40, self.posY*50+40,fill='black', width=1)
            self.canvas.create_oval(self.posX*50+8, self.posY*50+11,self.posX*50+28, self.posY*50+31,fill=col, width=1)
            self.canvas.create_oval(self.posX*50+18, self.posY*50+21,self.posX*50+38, self.posY*50+41,fill=col, width=1)
            self.canvas.create_oval(self.posX*50+20, self.posY*50+28,self.posX*50+40, self.posY*50+8,fill=col, width=1)
        
    def split(self):
        if(self.capacity == 1):
            self.canvas.create_oval(self.posX*50+15, self.posY*50+15,self.posX*50+35, self.posY*50+35,fill='black', width=1)
        elif(self.capacity == 2):
            self.canvas.create_oval(self.posX*50+10, self.posY*50+10,self.posX*50+30, self.posY*50+30,fill='black', width=1)
            self.canvas.create_oval(self.posX*50+20, self.posY*50+20,self.posX*50+40, self.posY*50+40,fill='black', width=1)
        elif(self.capacity == 3):
            self.canvas.create_oval(self.posX*50+8, self.posY*50+11,self.posX*50+28, self.posY*50+31,fill='black', width=1)
            self.canvas.create_oval(self.posX*50+18, self.posY*50+21,self.posX*50+38, self.posY*50+41,fill='black', width=1)
            self.canvas.create_oval(self.posX*50+20, self.posY*50+28,self.posX*50+40, self.posY*50+8,fill='black', width=1)
            
class GameWindow():
    def __init__(self):
        self.root = tki.Tk()
        self.root.title('Chain Reaction')
        self.root.geometry('400x400')
        self.canvas = tki.Canvas(self.root, width = 400, height = 400, bg = 'black')
        self.canvas.pack()
        
        #variables for storing mouse click coordinates
        self.mouseX = 0
        self.mouseY = 0
        self.player = 1     #Decides the current player
        self.grid = None    #contains the 2d array of grids
        
        self.root.bind('<Button 1>', self.getMousePosition)
        self.initGrid()
        
    def start(self):
        self.root.mainloop()
    
    def drawGrid(self):
        '''
        function to draw the grid on the canvas
        based on current player color
        '''
        if(self.player == 1):
            col = 'green'
        elif(self.player == 2):
            col = 'red'
        
        #Draws the straight line for the grid
        for i in range(8):
            self.canvas.create_line(0, i*50, 400, i*50, fill = col)
            self.canvas.create_line(i*50, 0, i*50, 400, fill = col)
            
    def getMousePosition(self, event):
        '''
        function to get the mouse position on click on the grid
        and start a move
        '''
        self.mouseX = event.x
        self.mouseY = event.y
        move(self)
        
    def changePlayer(self):
        '''
        function to change the turn
        '''
        if(self.player == 1):
            self.player = 2
        elif(self.player == 2):
            self.player = 1
    
    def initGrid(self):
        '''
        function to initialize 2d array of grid
        '''
        self.grid = [None]*8
        for i in range(8):
            self.grid[i] = [None]*8
            
        for i in range(8):
            for j in range(8):
                self.grid[i][j] = Grid(self.canvas, i,j)
        
if __name__ == '__main__':        
    win = GameWindow()
    win.drawGrid()
    win.start()