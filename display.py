from Tkinter import *
from bsocket import BSocket
import socket 

PORT = 1234


class Display(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', PORT))
        self.bsocket = BSocket(self.socket)
        self.bsocket.sendDimensions(height, width)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getValue(self, x, y):
        self.bsocket.sendUpdate("r", x, y, 0)
        return self.bsocket.readColor()

    def setValue(self, x, y, c):
        self.bsocket.sendUpdate("u", x, y, c)

    def drawRectangle(self, x, y, w, h, c):
        if x + w >= self.getWidth() or y + h >= self.getHeight() or x < 0 or y < 0:
            print "ERROR: OUT OF BOUNDS"
            return None
       
        for i in range(x, x + w):
            for j in range(y, y + h):
                self.setValue(i, j, c)

    def drawTriangle(self, x, y, w, h, c):
        if x + w >= self.getWidth() or y + h >= self.getHeight() or x < 0 or y < 0:
            print "ERROR: OUT OF BOUNDS"
            return None

        for i in range(x, x + w, w/abs(w)):
            for j in range(y, y + h - int(round((i - x) * h/w)), h/abs(h)):
                self.setValue(i, j, c)

    def clear(self):
        self.drawRectangle(0, 0, self.getWidth(), self.getHeight(), 0)
