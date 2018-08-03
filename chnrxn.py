# Python program for 2 player version of the android game chain reaction using tkinter
import tkinter as tki

def chain_reaction(gameWindow):
    print('hello')
    
class GameWindow():
    def __init__(self):
        self.root = tki.Tk()
        self.root.title('Chain Reaction')
        self.root.geometry('400x400')
        self.canvas = tki.Canvas(self.__root, width = 400, height = 400, bg = 'black')
        self.canvas.pack()
        
        #variables for storing mouse click coordinates
        self.mouseX = 0
        self.mouseY = 0
        self.root.bind('<Button 1>', self.getMousePosition)
        
    def start(self):
        self.root.mainloop()
    
    def drawGrid(self, col):
        for i in range(8):
            self.canvas.create_line(0, i*50, 400, i*50, fill = col)
            self.canvas.create_line(i*50, 0, i*50, 400, fill = col)
            
    def getMousePosition(self, event):
        self.mouseX = event.x
        self.mouseY = event.y
        move()
        
        
if __name__ == '__main__':        
    win = GameWindow()
    win.drawGrid('green')
    win.start()