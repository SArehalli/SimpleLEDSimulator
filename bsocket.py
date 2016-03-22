import socket

class BSocket(object):
    """ Wrapper for sockets to deal with LED board communications """

    DIMENSIONS = "{:2};{:2}"
    UPDATE     = "{:1};{:2};{:2};{:#8X}"
    COLOR      = "{:#6X}"
    LEN_DIM    = len(DIMENSIONS.format(0,0))
    LEN_UP     = len(UPDATE.format("r",0,0,0))
    LEN_COLOR  = len(COLOR.format(0))


    def __init__(self, s):
        self.socket = s

    def send(self, msg):
        length = len(msg)
        tsent = 0

        while tsent < length:
            sent = self.socket.send(msg[tsent:])
            if not sent:
                raise RuntimeError("Connection Broken")
            tsent += sent


    def sendDimensions(self, h, w):
        self.send(self.DIMENSIONS.format(h,w))

    def sendUpdate(self, m, x, y, c):
        self.send(self.UPDATE.format(m, x, y, c))

    def sendColor(self, c):
        self.send(self.COLOR.format(c))

    def read(self, length):
        tread = 0
        tmsg = [] 

        while tread < length:
            msg = self.socket.recv(min(length - tread, 2048))
            
            if not len(msg):
                raise RuntimeError("Connection Broken")
            
            tread += len(msg)
            tmsg.append(msg)

        return "".join(tmsg)

    def readDimensions(self):
        msg = self.read(self.LEN_DIM).split(";")
        return tuple(map(int, msg))

    def readUpdate(self):
        msg = self.read(self.LEN_UP).split(";")
        return tuple([msg[0]] + map(int, msg[1:-1]) + [int(msg[-1], 16)])

    def readColor(self):
        msg = self.read(self.LEN_COLOR)
        return int(msg, 16)

            
