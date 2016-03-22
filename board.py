from Tkinter import *
from bsocket import BSocket
import threading
import Queue
import socket

PIXEL_WIDTH = 10
EMPTY_COLOR = "#000000"
PORT = 1234

class BoardGUI(object):
    """ Actual GUI you see """
    
    def __init__(self, master, queue, height, width):
        self.queue = queue
        self.height = height
        self.width = width

        self.master = master
        self.canvas = Canvas(self.master, width=PIXEL_WIDTH * width, \
                                          height=PIXEL_WIDTH * height)
        self.canvas.pack();
        
        self.grid = [[None for j in range(height)] for i in range(width)]
        
        for i in range(width):
            for j in range(height):
                self.grid[i][height - j - 1] = self.canvas.create_rectangle(i * PIXEL_WIDTH, \
                                                               j * PIXEL_WIDTH, \
                                                               (i + 1) * PIXEL_WIDTH, \
                                                               (j + 1) * PIXEL_WIDTH, \
                                                               fill = EMPTY_COLOR)

    def processIncoming(self):
        while self.queue.qsize():
            try: 
                (x, y, c) = self.queue.get(0)
                self.setValue(x, y, c)
                #print "UPDATE: at {}, {} with color {}".format(x,y,self.__hex2Color(c))

            except Queue.Empty:
                pass


    def __hex2Color(self, c):
        return "#{:0>6}".format(hex(c & 0xFFFFFF)[2:])

    def setValue(self, x, y, c):
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            print "ERROR: OUT OF BOUNDS"
            return None
        self.canvas.itemconfig(self.grid[x][y], fill=self.__hex2Color(c))
        self.canvas.update_idletasks()

class LEDBoard:
    """ GUI + message handler. """

    def __init__(self, master):
        self.master = master

        self.queue = Queue.Queue()

        ### Sockets ###
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', PORT))
        s.listen(1)

        print "LOOKING FOR CONNECTION"
        (cs, address) = s.accept()
        print "CONNECTION FOUND"
        cbs = BSocket(cs) 
        
        (height, width) = cbs.readDimensions()
        print "RECIEVED DIMENSIONS: {} x {}".format(height, width)
        self.gui = BoardGUI(master, self.queue, height, width)

        self.thread = threading.Thread(target=self.listen, args=(cbs,))
        self.thread.start()

        self.master.after(200, self.guiUpdate)

    def listen(self, bs):
        while 1:
            (m, x, y, c) = bs.readUpdate()
            #print "READ/UPDATE REQUESTED: code {} at {}, {} with color {}".format(m, x, y, c)
            if m == "r":
                color = self.gui.canvas.itemcget(self.gui.grid[x][y], "fill")[1:]
                bs.sendColor(int(color, 16))
            else:
                self.queue.put((x, y, c))

    def guiUpdate(self):
        self.gui.processIncoming()
        self.master.after(200, self.guiUpdate)

if __name__ == "__main__":
    root = Tk()
    LB = LEDBoard(root)
    root.mainloop()
