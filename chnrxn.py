# Python program for 2 player version of the android game chain reaction using tkinter
import tkinter as tki
import time
import queue

def chain_reaction(win, x, y):
    '''
    function to implement the gameplay mechanics
    '''
    gridQueue = queue.Queue()
    gridQueue.put(win.grid[x][y])
    while gridQueue.empty() == False:
        cur = gridQueue.get()
        #Case : Grid is empty
        if cur.owner == 9:
            win.owned[0] -= 1
            win.owned[win.player] += 1
            cur.owner = win.player
            cur.orb = 1
            cur.draw()
        #Case : Grid is not empty
        else:
            if cur.owner != win.player:
                win.owned[cur.owner] -= 1
                win.owned[win.player] += 1
                cur.owner = win.player
                cur.draw()
                
            cur.orb += 1
            if cur.orb > cur.capacity:
                cur.split()
                cur.owner = 9
                win.owned[0] += 1
                win.owned[win.player] -= 1
                #top left grid
                if cur.type == 1:
                    gridQueue.put(win.grid[cur.posX+1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY+1])
                
                #bottom left grid
                elif cur.type == 2:
                    gridQueue.put(win.grid[cur.posX+1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY-1])
                    
                #top right grid
                elif cur.type == 3:
                    gridQueue.put(win.grid[cur.posX-1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY+1])
                    
                #bottom right grid
                elif cur.type == 4:
                    gridQueue.put(win.grid[cur.posX-1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY-1])
                    
                #first row grids
                elif cur.type == 5:
                    gridQueue.put(win.grid[cur.posX+1][cur.posY])
                    gridQueue.put(win.grid[cur.posX-1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY+1])
                    
                #last row grids
                elif cur.type == 6:
                    gridQueue.put(win.grid[cur.posX+1][cur.posY])
                    gridQueue.put(win.grid[cur.posX-1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY-1])
                    
                #first column grids
                elif cur.type == 7:
                    gridQueue.put(win.grid[cur.posX+1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY-1])
                    gridQueue.put(win.grid[cur.posX][cur.posY+1])
                    
                #last column grids
                elif cur.type == 8:
                    gridQueue.put(win.grid[cur.posX-1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY-1])
                    gridQueue.put(win.grid[cur.posX][cur.posY+1])
                    
                #middle grids
                else:
                    gridQueue.put(win.grid[cur.posX+1][cur.posY])
                    gridQueue.put(win.grid[cur.posX-1][cur.posY])
                    gridQueue.put(win.grid[cur.posX][cur.posY+1])
                    gridQueue.put(win.grid[cur.posX][cur.posY-1])
            else:
                cur.draw()
                
            
            
            
def move(win):
    x = win.mouseX//50
    y = win.mouseY//50
    #invalid move
    if win.grid[x][y].owner != 9 and win.grid[x][y].owner != win.player:
        return
    
    chain_reaction(win, x, y)
    win.turn += 1
    if(win.turn > 2):
        if win.owned[1] == 0 or win.owned[2] == 0:
            win.canvas.delete('all')
            if win.player == 1:
                col = 'green'
            else:
                col = 'red'
                
            win.canvas.create_text(190,180, fill=col, font=('Consolas', 20), text = "Player "+str(win.player)+" wins !")
            win.finished = True
            return
        
    win.changePlayer()
    win.drawGrid()
    
class Grid():
    def __init__(self, canvas, xVal, yVal):
        self.capacity = self.getCapacity(xVal, yVal)      #sets the capacity of the grid
        self.owner = 9                          #default owner of grid is nobody
        self.orb = 0                            #holds the number of orbs in the cell
        self.orbList = []                       #holds the actual orbs in the cell
        self.posX = xVal                        #holds x coordinate of the grid 
        self.posY = yVal                        #holds y coordinate of the grid
        self.type = self.getType(xVal, yVal)    #holds the type of the grid
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
    
    def getType(self,x,y):
        '''
        returns the type of grid based on position
        '''
        if(self.capacity == 1):
            #top left grid
            if(x == 0 and y == 0):
                return 1
            
            #bottom left grid
            elif(x == 0 and y == 7):
                return 2
            
            #top right grid
            elif(x == 7 and y == 0):
                return 3
            
            #bottom right grid
            else:
                return 4
            
        elif(self.capacity == 2):
            #first row grids
            if(y == 0):
                return 5
            
            #last row grids
            if(y == 7):
                return 6
            
            #first column grids
            if(x == 0):
                return 7
            
            #last column grids
            if(x == 7):
                return 8
            
        else:
            #middle grids
            return 9
    
    def setOwner(self, val):
        '''
        sets the owner of the grid
        '''
        self.owner = val
        
    def resetOwner(self):
        '''
        resets the owner of the grid
        '''
        self.owner = 9
    
    def getColor(self):
        '''
        Returns color for drawing orbs according to
        the owner of the grid
        '''
        if(self.owner == 1):
            return 'green'
        elif(self.owner == 2):
            return 'red'
    
    def reset(self):
        '''
        clears grid list and removes orbs from board
        '''
        #delete previous orbs from game-board
        for i in range(len(self.orbList)):
            self.canvas.delete(self.orbList[i])
            
        self.orbList = []   #clear the orb list
        
    def draw(self):
        '''
        function to draw orbs inside the grid
        '''
        col = self.getColor()
        self.reset()
        
        if(self.orb == 1):
            self.orbList.append(self.canvas.create_oval(self.posX*50+15, self.posY*50+15,self.posX*50+35, self.posY*50+35,fill=col, width=1))
        elif(self.orb == 2):
            self.orbList.append(self.canvas.create_oval(self.posX*50+10, self.posY*50+10,self.posX*50+30, self.posY*50+30,fill=col, width=1))
            self.orbList.append(self.canvas.create_oval(self.posX*50+20, self.posY*50+20,self.posX*50+40, self.posY*50+40,fill=col, width=1))
        elif(self.orb == 3):
            self.orbList.append(self.canvas.create_oval(self.posX*50+8, self.posY*50+11,self.posX*50+28, self.posY*50+31,fill=col, width=1))
            self.orbList.append(self.canvas.create_oval(self.posX*50+18, self.posY*50+21,self.posX*50+38, self.posY*50+41,fill=col, width=1))
            self.orbList.append(self.canvas.create_oval(self.posX*50+20, self.posY*50+28,self.posX*50+40, self.posY*50+8,fill=col, width=1))
        
    def split(self):
        tm = 0.005 #time to delay
        self.orbList.append(self.canvas.create_oval(self.posX*50+15, self.posY*50+15,self.posX*50+35, self.posY*50+35,fill=self.getColor(), width=1))
        #top left grid
        if(self.type == 1):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,1)
                self.canvas.move(self.orbList[1],1,0)
                self.canvas.update()
            
        #bottom left grid
        elif(self.type == 2):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,-1)
                self.canvas.move(self.orbList[1],1,0)
                self.canvas.update()
            
        #top right grid
        elif(self.type == 3):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,1)
                self.canvas.move(self.orbList[1],-1,0)
                self.canvas.update()
            
        #bottom right grid
        elif(self.type == 4):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,-1)
                self.canvas.move(self.orbList[1],-1,0)
                self.canvas.update()
                    
        #first row grids
        elif(self.type == 5):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],-1,0)
                self.canvas.move(self.orbList[1],0,1)
                self.canvas.move(self.orbList[2],1,0)
                self.canvas.update()
                
        #last row grids
        elif(self.type == 6):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,-1)
                self.canvas.move(self.orbList[1],-1,0)
                self.canvas.move(self.orbList[2],1,0)
                self.canvas.update()
        
        #first column grids
        elif(self.type == 7):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,1)
                self.canvas.move(self.orbList[1],0,-1)
                self.canvas.move(self.orbList[2],1,0)
                self.canvas.update()
        
        #last column grids
        elif(self.type == 8):
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,-1)
                self.canvas.move(self.orbList[1],0,1)
                self.canvas.move(self.orbList[2],-1,0)
                self.canvas.update()
        
        #middle grids
        else:
            for i in range(45):
                time.sleep(tm)
                self.canvas.move(self.orbList[0],0,-1)
                self.canvas.move(self.orbList[1],-1,0)
                self.canvas.move(self.orbList[2],1,0)
                self.canvas.move(self.orbList[3],0,1)
                self.canvas.update()
                
        #reset the grid
        self.reset()
        self.orb = 0
                
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
        self.turn = 0       #number of turns
        self.owned = [64, 0, 0] #list of number of grids owned
        self.root.bind('<Button 1>', self.getMousePosition)
        self.initGrid()
        self.finished = False   #variable to decide if the game has finished
        
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
        if self.finished == True:
            self.root.destroy()
            return
        
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